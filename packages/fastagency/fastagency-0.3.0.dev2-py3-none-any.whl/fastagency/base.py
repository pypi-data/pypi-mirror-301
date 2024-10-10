import inspect
from collections.abc import Awaitable, Generator, Iterable, Iterator, Mapping
from contextlib import contextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)

from .messages import (
    MessageProcessorProtocol,
)

if TYPE_CHECKING:
    from fastagency.api.openapi import OpenAPI

__all__ = [
    "UI",
    "WSGIProtocol",
    "ASGIProtocol",
    "ProviderProtocol",
    "WorkflowsProtocol",
    "AdapterProtocol",
    "Runnable",
    "Workflow",
    "Agent",
    "run_workflow",
]


@runtime_checkable
class UI(MessageProcessorProtocol, Protocol):
    @contextmanager
    def create(self, app: "Runnable", import_string: str) -> Iterator[None]: ...

    def start(
        self,
        *,
        app: "Runnable",
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None: ...

    # def process_streaming_message(
    #     self, message: IOStreamingMessage
    # ) -> Optional[str]: ...

    def create_subconversation(self) -> "UI": ...


@runtime_checkable
class WSGIProtocol(Protocol):
    def handle_wsgi(
        self,
        app: "Runnable",
        environ: dict[str, Any],
        start_response: Callable[..., Any],
    ) -> list[bytes]: ...


@runtime_checkable
class ASGIProtocol(Protocol):
    async def handle_asgi(
        self,
        app: "Runnable",
        scope: dict[str, Any],
        receive: Callable[[dict[str, Any]], Awaitable[None]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None: ...


# signature of a function decorated with @wf.register
# Workflow = TypeVar("Workflow", bound=Callable[["WorkflowsProtocol", UI, str, str], str])
# parameters are: WorkflowsProtocol, UI, workflow_uuid, params (kwargs)
Workflow = TypeVar("Workflow", bound=Callable[[UI, str, dict[str, Any]], str])


Agent = TypeVar("Agent")


@runtime_checkable
class ProviderProtocol(Protocol):
    def run(self, name: str, ui: UI, **kwargs: Any) -> str: ...

    """Run a workflow.

    Creates a new workflow and assigns it workflow_uuid. Then it calls the
    workflow function (function decorated with @wf.register) with the given
    ui and workflow_uuid.

    Args:
        name (str): The name of the workflow to run.
        ui (UI): The UI object to use.
        **kwargs: Additional parameters to pass to the workflow function.
    """

    @property
    def names(self) -> list[str]: ...

    def get_description(self, name: str) -> str: ...


@runtime_checkable
class WorkflowsProtocol(ProviderProtocol, Protocol):
    def register(
        self, name: str, description: str
    ) -> Callable[[Workflow], Workflow]: ...

    def register_api(
        self,
        api: "OpenAPI",
        callers: Union[Agent, Iterable[Agent]],
        executors: Union[Agent, Iterable[Agent]],
        functions: Optional[
            Union[str, Iterable[Union[str, Mapping[str, Mapping[str, str]]]]]
        ] = None,
    ) -> None: ...


def check_register_decorator(func: Workflow) -> None:
    # get names of all parameters in the function signature
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    if params != ["ui", "workflow_uuid", "params"]:
        raise ValueError(
            f"Expected function signature to be 'def func(ui: UI, workflow_uuid: str, params: dict[str, Any]) -> str', got {sig}"
        )


@runtime_checkable
class AdapterProtocol(Protocol):
    @classmethod
    def create_provider(*args: Any, **kwargs: Any) -> ProviderProtocol: ...


@runtime_checkable
class Runnable(Protocol):
    @contextmanager
    def create(self, import_string: str) -> Generator[None, None, None]: ...

    def start(
        self,
        *,
        import_string: str,
        name: Optional[str] = None,
        params: dict[str, Any],
        single_run: bool = False,
    ) -> None: ...

    @property
    def provider(self) -> ProviderProtocol: ...

    @property
    def ui(self) -> UI: ...

    @property
    def title(self) -> str: ...

    @property
    def description(self) -> str: ...


def run_workflow(
    *,
    provider: ProviderProtocol,
    ui: UI,
    name: Optional[str],
    params: dict[str, Any],
    single_run: bool = False,
) -> None:
    """Run a workflow.

    Args:
        provider (ProviderProtocol): The provider to use.
        ui (UI): The UI object to use.
        name (Optional[str]): The name of the workflow to run. If not provided, the default workflow will be run.
        params (dict[str, Any]): Additional parameters to pass to the workflow function.
        single_run (bool, optional): If True, the workflow will only be run once. Defaults to False.
    """
    while True:
        name = provider.names[0] if name is None else name
        description = provider.get_description(name)

        ui.workflow_started(
            sender="FastAgency",
            recipient="user",
            name=name,
            description=description,
            params=params,
        )

        result = provider.run(
            name=name,
            ui=ui.create_subconversation(),
            **params,
        )

        ui.workflow_completed(
            sender="workflow",
            recipient="user",
            result=result,
        )

        if single_run:
            break
