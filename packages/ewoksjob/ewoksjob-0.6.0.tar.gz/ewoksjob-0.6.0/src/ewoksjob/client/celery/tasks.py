import warnings
from celery.execute import send_task
from celery.result import AsyncResult
from ..dummy_workflow import dummy_workflow

__all__ = [
    "execute_graph",
    "execute_test_graph",
    "convert_graph",
    "convert_workflow",
    "discover_tasks_from_modules",
    "discover_all_tasks",
]


def execute_graph(**kw) -> AsyncResult:
    return send_task("ewoksjob.apps.ewoks.execute_graph", **kw)


def execute_test_graph(
    seconds=0, filename=None, args=None, kwargs=None, **kw
) -> AsyncResult:
    if args:
        raise TypeError("execute_test_graph does not take position arguments")
    args = (dummy_workflow(),)
    if kwargs is None:
        kwargs = dict()
    kwargs["inputs"] = [
        {"id": "sleep", "name": 0, "value": seconds},
        {"id": "result", "name": "filename", "value": filename},
    ]
    return execute_graph(args=args, kwargs=kwargs, **kw)


def convert_graph(**kw) -> AsyncResult:
    return send_task("ewoksjob.apps.ewoks.convert_graph", **kw)


def convert_workflow(**kw) -> AsyncResult:
    warnings.warn(
        "convert_workflow is deprecated, use convert_graph instead", stacklevel=2
    )
    return convert_graph(**kw)


def discover_tasks_from_modules(**kw) -> AsyncResult:
    return send_task("ewoksjob.apps.ewoks.discover_tasks_from_modules", **kw)


def discover_all_tasks(**kw) -> AsyncResult:
    return send_task("ewoksjob.apps.ewoks.discover_all_tasks", **kw)
