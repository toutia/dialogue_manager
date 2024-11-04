from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Dict, List, Text

        
class ActionFindObject(Action):
    def name(self) -> Text:
        return "action_find_object"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        object_to_find = tracker.get_slot("object")
       
        # start the detection server here 
        # send object as global param {obj:obj, mode: detection}
        
        # If confirmed, proceed with object location guidance
        dispatcher.utter_message(
            text=f"Looking for the {object_to_find}. Move around slowly to help me locate it."
        )
        # Optionally provide further instructions or guidance
        dispatcher.utter_message(
            text="I will notify you when I find the object."
        )

        location = "table"
        direction = "left"
        distance = "a few feet"

        events = [
            SlotSet("object", object_to_find),
            SlotSet("object_distance", distance),
            SlotSet("object_direction", direction),
            SlotSet("object_location", location),
        ]

        # Respond to the user with the object location details
        response_text = f"I found the {object_to_find}. It's about {distance} meters away to the {direction}, located {location}."
        dispatcher.utter_message(text=response_text)

        return events

class ActionConfirmObject(Action):
    def name(self) -> str:
        return "action_confirm_object"

    def run(self, dispatcher, tracker, domain):
        # Set the object_confirmed slot to True when the user affirms
        object_to_find = tracker.get_slot("object")
         # Check if the object is confirmed by the user

        if not object_to_find:
            message_text=f"Could you please tell me what you're looking for? Please be specific."
            
        else :
            message_text= f"Are you looking for {object_to_find}? Please confirm."
        dispatcher.utter_message(
            text= message_text
        )
        return []



class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        # Calls utter_default, which will select from the list of responses in domain.yml
        dispatcher.utter_message(response="utter_default")
        return [UserUtteranceReverted()]




