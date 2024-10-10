"""Type definitions for the Redux store operations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from immutable import Immutable
from redux import BaseAction, BaseEvent

if TYPE_CHECKING:
    from ubo_app.store.services.notifications import NotificationExtraInformation


class ScreenshotEvent(BaseEvent):
    """Event for taking a screenshot."""


class SnapshotEvent(BaseEvent):
    """Event for taking a snapshot of the store."""


class InputDescription(Immutable):
    """Description of an input demand."""

    title: str
    prompt: str | None
    extra_information: NotificationExtraInformation | None = None
    id: str
    pattern: str | None


class InputAction(BaseAction):
    """Base class for input actions."""


class InputDemandAction(InputAction):
    """Action for demanding input from the user."""

    description: InputDescription


class InputProvideAction(InputAction):
    """Action for reporting input from the user."""

    id: str
    value: str
    data: dict[str, str | None] | None


class InputProvideEvent(BaseEvent):
    """Event for reporting input from the user."""

    id: str
    value: str
    data: dict[str, str | None] | None
