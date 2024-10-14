from injector import inject

from griff.appli.event.event import Event
from griff.appli.event.event_dispatcher import EventDispatcher, AppEventDispatcher
from griff.appli.event.event_handler import EventHandler, AppEventHandler
from griff.appli.message.message_bus import MessageBus


class EventBus(MessageBus[Event, None, EventHandler]):
    @inject
    def __init__(self, dispatcher: EventDispatcher) -> None:
        super().__init__(dispatcher)


class AppEventBus(MessageBus[Event, None, AppEventHandler]):
    @inject
    def __init__(self, dispatcher: AppEventDispatcher) -> None:
        super().__init__(dispatcher)
