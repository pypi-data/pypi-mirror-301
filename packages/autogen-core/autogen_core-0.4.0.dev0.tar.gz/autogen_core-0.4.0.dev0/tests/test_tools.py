import inspect
from typing import Annotated

import pytest
from autogen_core.base import CancellationToken
from autogen_core.components._function_utils import get_typed_signature
from autogen_core.components.models._openai_client import convert_tools
from autogen_core.components.tools import BaseTool, FunctionTool
from pydantic import BaseModel, Field, model_serializer
from pydantic_core import PydanticUndefined


class MyArgs(BaseModel):
    query: str = Field(description="The description.")


class MyResult(BaseModel):
    result: str = Field(description="The other description.")


class MyTool(BaseTool[MyArgs, MyResult]):
    def __init__(self) -> None:
        super().__init__(
            args_type=MyArgs,
            return_type=MyResult,
            name="TestTool",
            description="Description of test tool.",
        )
        self.called_count = 0

    async def run(self, args: MyArgs, cancellation_token: CancellationToken) -> MyResult:
        self.called_count += 1
        return MyResult(result="value")


def test_tool_schema_generation() -> None:
    schema = MyTool().schema

    assert schema["name"] == "TestTool"
    assert "description" in schema
    assert schema["description"] == "Description of test tool."
    assert "parameters" in schema
    assert schema["parameters"]["type"] == "object"
    assert "properties" in schema["parameters"]
    assert schema["parameters"]["properties"]["query"]["description"] == "The description."
    assert schema["parameters"]["properties"]["query"]["type"] == "string"
    assert "required" in schema["parameters"]
    assert schema["parameters"]["required"] == ["query"]
    assert len(schema["parameters"]["properties"]) == 1


def test_func_tool_schema_generation() -> None:
    def my_function(arg: str, other: Annotated[int, "int arg"], nonrequired: int = 5) -> MyResult:
        return MyResult(result="test")

    tool = FunctionTool(my_function, description="Function tool.")
    schema = tool.schema

    assert schema["name"] == "my_function"
    assert "description" in schema
    assert schema["description"] == "Function tool."
    assert "parameters" in schema
    assert schema["parameters"]["type"] == "object"
    assert schema["parameters"]["properties"].keys() == {"arg", "other", "nonrequired"}
    assert schema["parameters"]["properties"]["arg"]["type"] == "string"
    assert schema["parameters"]["properties"]["arg"]["description"] == "arg"
    assert schema["parameters"]["properties"]["other"]["type"] == "integer"
    assert schema["parameters"]["properties"]["other"]["description"] == "int arg"
    assert schema["parameters"]["properties"]["nonrequired"]["type"] == "integer"
    assert schema["parameters"]["properties"]["nonrequired"]["description"] == "nonrequired"
    assert "required" in schema["parameters"]
    assert schema["parameters"]["required"] == ["arg", "other"]
    assert len(schema["parameters"]["properties"]) == 3


def test_func_tool_schema_generation_only_default_arg() -> None:
    def my_function(arg: str = "default") -> MyResult:
        return MyResult(result="test")

    tool = FunctionTool(my_function, description="Function tool.")
    schema = tool.schema

    assert schema["name"] == "my_function"
    assert "description" in schema
    assert schema["description"] == "Function tool."
    assert "parameters" in schema
    assert len(schema["parameters"]["properties"]) == 1
    assert schema["parameters"]["properties"]["arg"]["type"] == "string"
    assert schema["parameters"]["properties"]["arg"]["description"] == "arg"
    assert "required" not in schema["parameters"]


@pytest.mark.asyncio
async def test_tool_run() -> None:
    tool = MyTool()
    result = await tool.run_json({"query": "test"}, CancellationToken())

    assert isinstance(result, MyResult)
    assert result.result == "value"
    assert tool.called_count == 1

    result = await tool.run_json({"query": "test"}, CancellationToken())
    result = await tool.run_json({"query": "test"}, CancellationToken())

    assert tool.called_count == 3


def test_tool_properties() -> None:
    tool = MyTool()

    assert tool.name == "TestTool"
    assert tool.description == "Description of test tool."
    assert tool.args_type() == MyArgs
    assert tool.return_type() == MyResult
    assert tool.state_type() is None


def test_get_typed_signature() -> None:
    def my_function() -> str:
        return "result"

    sig = get_typed_signature(my_function)
    assert isinstance(sig, inspect.Signature)
    assert len(sig.parameters) == 0
    assert sig.return_annotation == str


def test_get_typed_signature_annotated() -> None:
    def my_function() -> Annotated[str, "The return type"]:
        return "result"

    sig = get_typed_signature(my_function)
    assert isinstance(sig, inspect.Signature)
    assert len(sig.parameters) == 0
    assert sig.return_annotation == Annotated[str, "The return type"]


def test_get_typed_signature_string() -> None:
    def my_function() -> "str":
        return "result"

    sig = get_typed_signature(my_function)
    assert isinstance(sig, inspect.Signature)
    assert len(sig.parameters) == 0
    assert sig.return_annotation == str


def test_func_tool() -> None:
    def my_function() -> str:
        return "result"

    tool = FunctionTool(my_function, description="Function tool.")
    assert tool.name == "my_function"
    assert tool.description == "Function tool."
    assert issubclass(tool.args_type(), BaseModel)
    assert issubclass(tool.return_type(), str)
    assert tool.state_type() is None


def test_func_tool_annotated_arg() -> None:
    def my_function(my_arg: Annotated[str, "test description"]) -> str:
        return "result"

    tool = FunctionTool(my_function, description="Function tool.")
    assert tool.name == "my_function"
    assert tool.description == "Function tool."
    assert issubclass(tool.args_type(), BaseModel)
    assert issubclass(tool.return_type(), str)
    assert tool.args_type().model_fields["my_arg"].description == "test description"
    assert tool.args_type().model_fields["my_arg"].annotation == str
    assert tool.args_type().model_fields["my_arg"].is_required() is True
    assert tool.args_type().model_fields["my_arg"].default is PydanticUndefined
    assert len(tool.args_type().model_fields) == 1
    assert tool.return_type() == str
    assert tool.state_type() is None


def test_func_tool_return_annotated() -> None:
    def my_function() -> Annotated[str, "test description"]:
        return "result"

    tool = FunctionTool(my_function, description="Function tool.")
    assert tool.name == "my_function"
    assert tool.description == "Function tool."
    assert issubclass(tool.args_type(), BaseModel)
    assert tool.return_type() == str
    assert tool.state_type() is None


def test_func_tool_no_args() -> None:
    def my_function() -> str:
        return "result"

    tool = FunctionTool(my_function, description="Function tool.")
    assert tool.name == "my_function"
    assert tool.description == "Function tool."
    assert issubclass(tool.args_type(), BaseModel)
    assert len(tool.args_type().model_fields) == 0
    assert tool.return_type() == str
    assert tool.state_type() is None


def test_func_tool_return_none() -> None:
    def my_function() -> None:
        return None

    tool = FunctionTool(my_function, description="Function tool.")
    assert tool.name == "my_function"
    assert tool.description == "Function tool."
    assert issubclass(tool.args_type(), BaseModel)
    assert tool.return_type() is None
    assert tool.state_type() is None


def test_func_tool_return_base_model() -> None:
    def my_function() -> MyResult:
        return MyResult(result="value")

    tool = FunctionTool(my_function, description="Function tool.")
    assert tool.name == "my_function"
    assert tool.description == "Function tool."
    assert issubclass(tool.args_type(), BaseModel)
    assert tool.return_type() is MyResult
    assert tool.state_type() is None


@pytest.mark.asyncio
async def test_func_call_tool() -> None:
    def my_function() -> str:
        return "result"

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({}, CancellationToken())
    assert result == "result"


@pytest.mark.asyncio
async def test_func_call_tool_base_model() -> None:
    def my_function() -> MyResult:
        return MyResult(result="value")

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({}, CancellationToken())
    assert isinstance(result, MyResult)
    assert result.result == "value"


@pytest.mark.asyncio
async def test_func_call_tool_with_arg_base_model() -> None:
    def my_function(arg: str) -> MyResult:
        return MyResult(result="value")

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({"arg": "test"}, CancellationToken())
    assert isinstance(result, MyResult)
    assert result.result == "value"


@pytest.mark.asyncio
async def test_func_str_res() -> None:
    def my_function(arg: str) -> str:
        return "test"

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({"arg": "test"}, CancellationToken())
    assert tool.return_value_as_string(result) == "test"


@pytest.mark.asyncio
async def test_func_base_model_res() -> None:
    def my_function(arg: str) -> MyResult:
        return MyResult(result="test")

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({"arg": "test"}, CancellationToken())
    assert tool.return_value_as_string(result) == '{"result": "test"}'


@pytest.mark.asyncio
async def test_func_base_model_custom_dump_res() -> None:
    class MyResultCustomDump(BaseModel):
        result: str = Field(description="The other description.")

        @model_serializer
        def ser_model(self) -> str:
            return "custom: " + self.result

    def my_function(arg: str) -> MyResultCustomDump:
        return MyResultCustomDump(result="test")

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({"arg": "test"}, CancellationToken())
    assert tool.return_value_as_string(result) == "custom: test"


@pytest.mark.asyncio
async def test_func_int_res() -> None:
    def my_function(arg: int) -> int:
        return arg

    tool = FunctionTool(my_function, description="Function tool.")
    result = await tool.run_json({"arg": 5}, CancellationToken())
    assert tool.return_value_as_string(result) == "5"


def test_convert_tools_accepts_both_func_tool_and_schema() -> None:
    def my_function(arg: str, other: Annotated[int, "int arg"], nonrequired: int = 5) -> MyResult:
        return MyResult(result="test")

    tool = FunctionTool(my_function, description="Function tool.")
    schema = tool.schema

    converted_tool_schema = convert_tools([tool, schema])

    assert len(converted_tool_schema) == 2
    assert converted_tool_schema[0] == converted_tool_schema[1]


def test_convert_tools_accepts_both_tool_and_schema() -> None:
    tool = MyTool()
    schema = tool.schema

    converted_tool_schema = convert_tools([tool, schema])

    assert len(converted_tool_schema) == 2
    assert converted_tool_schema[0] == converted_tool_schema[1]
