from typing import Callable , Dict , List, Any 

class EventBus: 
    def __init__(self):
        self._subs:Dict[str,List[Callable[[Any],None]]] = {}

    def subscribe (self, event_name:str,handler:Callable[[any], None]= None) -> None:
            self._subs.setdefault(event_name, []).append (handler)
    def publish (self, event_name:str, payload: Any = None) ->None:
         for handler in self._subs.get(event_name,[]):
              handler (payload)

        