from typing import Any, Dict, List, Literal, Optional, Union, cast

from pydantic import BaseModel, Field, root_validator
from transformers import PreTrainedTokenizerFast


class ModelInput(BaseModel):

    # TODO: should support tool call id and tool
    class Message(BaseModel):
        """An element in the top level `messages` field."""

        role: str
        content: str

    class Tool(BaseModel):
        """An element in the top level `tools` field."""

        class Function(BaseModel):
            name: str
            description: str
            parameters: Dict[str, Any]  # parameters holds the json schema
            return_: Optional[Dict[str, Any]] = Field(None, alias="return")

        type: Literal["function"]
        function: Function

        @property
        def json_schema(self) -> Dict[str, Any]:
            return {
                "type": "object",
                "properties": {
                    "name": {"const": self.function.name},
                    "parameters": self.function.parameters,
                },
                "required": ["name", "parameters"],
            }

    class ToolChoice(BaseModel):
        """The top level `tool_choice` field."""

        class FunctionChoice(BaseModel):
            name: str

        type: Literal["function"]
        function: FunctionChoice

    class ResponseFormat(BaseModel):
        """The top level `response_format` field."""

        class JsonSchema(BaseModel):
            schema_: Dict[str, Any] = Field(..., alias="schema")  # schema holds the json schmea

        type: Literal["json_schema"]
        json_schema: JsonSchema

    prompt_: Optional[str] = Field(None, min_length=1, alias="prompt")
    messages: Optional[List[Message]] = Field(None)
    response_format: Optional[ResponseFormat] = Field(None)
    tools_: Optional[List[Tool]] = Field(None, alias="tools")
    tool_choice: Optional[Union[Literal["none", "required", "auto"], ToolChoice]] = Field(None)
    beam_width: Optional[Literal[1]] = Field(None)

    @root_validator(skip_on_failure=True)  # type: ignore
    def messages_not_empty(cls, values):
        messages = values.get("messages")
        if messages is not None and len(messages) == 0:
            raise ValueError("`messages` cannot be empty.")
        return values

    @root_validator(skip_on_failure=True)  # type: ignore
    def messages_and_prompt_not_set(cls, values):
        prompt = values.get("prompt_")
        messages = values.get("messages")
        if prompt is not None and messages is not None:
            raise ValueError("Only one of `prompt` and `messages` can be specified.")
        return values

    @root_validator(skip_on_failure=True)  # type: ignore
    def tools_valid(cls, values):
        tools = values.get("tools_")
        tool_choice = values.get("tool_choice")
        if tools is not None and tool_choice is None:
            raise ValueError("`tool_choice` must be specified if `tools` are specified.")
        if tools is not None and len(tools) == 0 and tool_choice != "none":
            raise ValueError("`tools` cannot be empty.")
        if isinstance(tool_choice, cls.ToolChoice) and tool_choice.function.name not in [
            tool.function.name for tool in tools
        ]:
            raise ValueError("`tool_choice` not in `tools`.")
        return values

    @root_validator(skip_on_failure=True)
    def tools_not_used_with_prompt(cls, values):
        prompt = values.get("prompt_")
        tool_choice = values.get("tool_choice")
        if prompt is not None and tool_choice is not None and tool_choice != "none":
            raise ValueError("`tool_choice` cannot be used with `prompt`.")
        return values

    @root_validator(skip_on_failure=True)
    def tools_not_used_with_response_format(cls, values):
        response_format = values.get("response_format")
        tool_choice = values.get("tool_choice")
        if response_format is not None and tool_choice is not None and tool_choice != "none":
            raise ValueError("`tools` cannot be used with `response_format`.")
        return values

    @property
    def has_tools(self) -> bool:
        return self.tool_choice is not None and self.tool_choice != "none"

    @property
    def force_tools(self) -> Optional[bool]:
        if self.has_tools:
            return self.tool_choice == "required" or isinstance(self.tool_choice, self.ToolChoice)
        return None

    @property
    def tools(self) -> Optional[List[Tool]]:
        """Returns the tools to use, dependent on tool_choice."""
        if self.tool_choice is not None and self.tool_choice != "none":
            assert self.tools_ is not None
            if isinstance(self.tool_choice, self.ToolChoice):
                return [
                    tool
                    for tool in self.tools_
                    if tool.function.name == self.tool_choice.function.name
                ]
            return self.tools_
        return None

    @property
    def output_json_schema(self) -> Optional[Dict[str, Any]]:
        """Creates the output json schema based on the response format or tools."""
        if self.response_format is not None:
            return self.response_format.json_schema.schema_
        tools = self.tools
        if tools is not None:
            return {
                "type": "array",
                "items": {"anyOf": [tool.json_schema for tool in tools]},
                "minItems": 1,
            }
        return None

    @property
    def message_dicts(self) -> Optional[List[Dict[str, str]]]:
        return [msg.dict() for msg in self.messages] if self.messages is not None else None

    @property
    def tool_dicts(self) -> Optional[List[Dict[str, Any]]]:
        return [tool.dict(by_alias=True) for tool in self.tools] if self.tools is not None else None

    def prompt(self, tokenizer: PreTrainedTokenizerFast) -> str:
        """Calculate text prompt from model_input.

        Prompt may be supplied in the input as such or as messages. If messages
        are supplied, they are used to generate the prompt using chat template.
        """
        if self.prompt_ is None:
            messages = self.message_dicts
            assert messages is not None
            return cast(
                str,
                tokenizer.apply_chat_template(
                    conversation=messages,
                    tools=self.tool_dicts,
                    tokenize=False,
                    add_generation_prompt=True,
                ),
            )
        return self.prompt_
