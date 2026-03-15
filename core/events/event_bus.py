import logging


logger = logging.getLogger(__name__)

_listeners = {}


def register(event_type, listener):
    listeners = _listeners.setdefault(event_type, [])

    if listener not in listeners:
        listeners.append(listener)


def emit(event_type, payload):
    if not isinstance(payload, dict):
        raise ValueError('Event payload must be a dict')
    listeners = _listeners.get(event_type, [])

    logger.debug(
        f"Dispatching event '{event_type}' to {len(listeners)} listeners"
    )

    if not listeners:
        logger.debug(f"No listeners registered for event {event_type}")
        return

    for listener in listeners:
        try:
            listener(payload)
        except Exception as e:
            logger.exception(
                "Event Listener Failure",
                extra={
                    "event_type": event_type,
                    "listener": listener.__name__,
                    "payload": payload,
                }
            )


