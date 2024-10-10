"""Input reducer."""

from __future__ import annotations

from redux import CompleteReducerResult, ReducerResult

from ubo_app.store.operations import InputAction, InputProvideAction, InputProvideEvent


def reducer(
    state: None,
    action: InputAction,
) -> ReducerResult[None, None, InputProvideEvent]:
    """Input reducer."""
    if isinstance(action, InputProvideAction):
        return CompleteReducerResult(
            state=state,
            events=[
                InputProvideEvent(
                    id=action.id,
                    value=action.value,
                    data=action.data,
                ),
            ],
        )

    return None
