import json
import sys
from datetime import date, datetime
from typing import Any

if sys.version_info < (3, 11):
    from backports.datetime_fromisoformat import MonkeyPatch  # type: ignore

    MonkeyPatch.patch_fromisoformat()


class _EvaluatorEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (date, datetime)):
            return {"__type__": "isoformat8601", "value": o.isoformat()}
        return json.JSONEncoder.default(self, o)


def evaluator_marshaller(content: Any) -> Any:
    if content is None:
        return None
    try:
        return json.dumps(content, cls=_EvaluatorEncoder)
    except TypeError:
        return content


def _object_hook(obj: Any) -> Any:
    if "__type__" not in obj:
        return obj

    if obj["__type__"] == "isoformat8601":
        return datetime.fromisoformat(obj["value"])

    return obj


def evaluator_unmarshaller(content: Any) -> Any:
    """
    Due to internals of CloudEvent content is double-encoded, therefore double-decoding
    """
    if content is None:
        return None
    try:
        content = json.loads(content)
        return json.loads(content, object_hook=_object_hook)
    except TypeError:
        return content
