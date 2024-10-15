# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ConfigExecuteParams", "Message"]


class ConfigExecuteParams(TypedDict, total=False):
    messages: Required[Optional[Iterable[Message]]]

    metadata: Required[Optional[object]]

    run_id: Required[Optional[str]]

    session_id: Required[str]

    id: str

    concurrent: Optional[bool]

    stream: bool


class Message(TypedDict, total=False):
    content: Required[str]

    role: Required[Literal["assistant", "user", "system"]]

    uuid: Annotated[str, PropertyInfo(alias="UUID")]
