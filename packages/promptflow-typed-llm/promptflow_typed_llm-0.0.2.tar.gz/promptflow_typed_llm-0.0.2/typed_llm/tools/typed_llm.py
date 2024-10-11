from typing import Union
from pathlib import Path
import importlib.util
import sys
import asyncio

from promptflow.core import tool
from promptflow.connections import AzureOpenAIConnection
from pydantic import BaseModel
from openai import AsyncAzureOpenAI, BadRequestError
from promptflow.contracts.types import FilePath
from promptflow.tools.common import handle_openai_error


MAX_CONCURRENT_REQUESTS = 4
# Has to be hardcoded because only the new API supports structured JSON API
API_VERSION = "2024-08-01-preview"


def _import_module(module_path: str):
    module_name = Path(module_path).stem
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def list_supported_response_formats(module_path: FilePath) -> list[dict[str, Union[str, int, float, list, dict]]]:
    """This is a function to load all possible response formats.
    Response formats are the ones of type pydantic.BaseModel in the specified module.

    :param parameters.
    :return: a list of items. Each item is a dict with the following keys:
        - value: for backend use. Required.
        - display_value: for UI display. Optional.
        - hyperlink: external link. Optional.
        - description: information icon tip. Optional.
    """
    # Load python module dynamically from model_module_path, 
    # then return all classes that inherit from BaseModel
    # Example:
    module = _import_module(module_path)
    return [{"value": cls.__name__, "display_value": cls.__name__} for cls in module.__dict__.values() if isinstance(cls, type) and issubclass(cls, BaseModel)]


@handle_openai_error()
async def _async_do_openai_request(
    client: AsyncAzureOpenAI, 
    semaphore: asyncio.Semaphore,
    deployment_name: str,
    temperature: float,
    messages: list[dict[str, str]],
    response_format: type):

    async with semaphore:
        completion = await client.beta.chat.completions.parse(
            model=deployment_name,
            response_format=response_format,
            temperature=temperature,
            messages=messages,
        )

        if completion.choices[0].message.refusal:
            raise BadRequestError(f"Completion refused: {completion.choices[0].message.refusal}")
        return completion.choices[0].message.content


@tool
def typed_llm(
    connection: AzureOpenAIConnection, 
    deployment_name: str,
    module_path: FilePath,
    response_type: list[str],
    temperature: float = 1,
    system_prompt: str | None = None,
    user_prompt: str | None = None,
    assistant_prompt: str | None = None,
    number_of_requests: int = 1,
    **kwargs) -> list[str]:

    if not system_prompt and not user_prompt and not assistant_prompt:
        raise BadRequestError("At least one of system_prompt, user_prompt, or assistant_prompt must be provided.")
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    if assistant_prompt:
        messages.append({"role": "assistant", "content": assistant_prompt})

    module = _import_module(module_path)
    if len(response_type) != 1 or response_type[0] not in module.__dict__:
        raise BadRequestError(f"response_type {response_type[0]} not found in {module_path}")
    response_format = module.__dict__[response_type[0]]

    async def do_requests():
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        client = AsyncAzureOpenAI(api_key=connection.api_key, azure_endpoint=connection.api_base, api_version=API_VERSION)

        tasks = [asyncio.create_task(_async_do_openai_request(
            client,
            semaphore,
            deployment_name,
            temperature,
            messages,
            response_format)) for _ in range(number_of_requests)]
        return await asyncio.gather(*tasks)
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(do_requests())