# ruff: noqa: D100, D101, D102, D103, D104, D107
from __future__ import annotations

import datetime
import re
from dataclasses import replace

from redux import (
    CompleteReducerResult,
    InitAction,
    InitializationActionError,
    ReducerResult,
)

from ubo_app.store.operations import (
    InputDemandAction,
    InputProvideAction,
)
from ubo_app.store.services.camera import (
    CameraEvent,
    CameraReportBarcodeAction,
    CameraStartViewfinderAction,
    CameraStartViewfinderEvent,
    CameraState,
    CameraStopViewfinderEvent,
)
from ubo_app.store.services.keypad import Key, KeypadKeyPressAction
from ubo_app.store.services.notifications import (
    Notification,
    NotificationDispatchItem,
    NotificationDisplayType,
    NotificationsAddAction,
)

Action = InitAction | InputDemandAction


def pop_queue(state: CameraState) -> CameraState:
    if len(state.queue) > 0:
        input_description, *queue = state.queue
        return replace(state, current=input_description, queue=queue)
    return replace(
        state,
        is_viewfinder_active=False,
        current=None,
    )


def reducer(
    state: CameraState | None,
    action: Action,
) -> ReducerResult[
    CameraState,
    Action | NotificationsAddAction | InputProvideAction,
    CameraEvent,
]:
    if state is None:
        if isinstance(action, InitAction):
            return CameraState(is_viewfinder_active=False, queue=[])
        raise InitializationActionError(action)

    if isinstance(action, InputDemandAction):
        if state.is_viewfinder_active:
            return replace(
                state,
                queue=[
                    *state.queue,
                    action.description,
                ],
            )
        return CompleteReducerResult(
            state=replace(
                state,
                is_viewfinder_active=True,
                current=action.description,
            ),
            actions=[
                NotificationsAddAction(
                    notification=Notification(
                        id='qrcode',
                        icon='󰄀󰐲',
                        title='QR Code',
                        content=f'[size=18dp]{action.description.prompt}[/size]',
                        display_type=NotificationDisplayType.STICKY,
                        is_read=True,
                        extra_information=action.description.extra_information,
                        expiration_timestamp=datetime.datetime.now(tz=datetime.UTC),
                        color='#ffffff',
                        actions=[
                            NotificationDispatchItem(
                                operation=CameraStartViewfinderAction(
                                    pattern=action.description.pattern,
                                ),
                                icon='󰄀',
                                dismiss_notification=True,
                            ),
                        ],
                        dismissable=False,
                        dismiss_on_close=True,
                    ),
                ),
            ],
        )

    if isinstance(action, InputProvideAction):
        if state.current and state.current.id == action.id:
            return CompleteReducerResult(
                state=pop_queue(state),
                events=[
                    CameraStopViewfinderEvent(id=state.current.id),
                ],
            )
        return replace(
            state,
            queue=[
                description
                for description in state.queue
                if description.id != action.id
            ],
        )

    if isinstance(action, CameraStartViewfinderAction):
        return CompleteReducerResult(
            state=state,
            events=[CameraStartViewfinderEvent(pattern=action.pattern)],
        )

    if isinstance(action, CameraReportBarcodeAction) and state.current:
        for code in action.codes:
            if state.current.pattern:
                match = re.match(state.current.pattern, code)
                if match:
                    return CompleteReducerResult(
                        state=pop_queue(state),
                        actions=[
                            InputProvideAction(
                                id=state.current.id,
                                value=code,
                                data=match.groupdict(),
                            ),
                        ],
                        events=[
                            CameraStopViewfinderEvent(id=None),
                        ],
                    )
            else:
                return CompleteReducerResult(
                    state=pop_queue(state),
                    actions=[
                        InputProvideAction(
                            id=state.current.id,
                            value=code,
                            data=None,
                        ),
                    ],
                    events=[
                        CameraStopViewfinderEvent(id=None),
                    ],
                )

            return state

    if isinstance(action, KeypadKeyPressAction):  # noqa: SIM102
        if action.key == Key.BACK and state.is_viewfinder_active:
            return CompleteReducerResult(
                state=pop_queue(state),
                events=[
                    CameraStopViewfinderEvent(
                        id=state.current.id if state.current else None,
                    ),
                ],
            )

    return state
