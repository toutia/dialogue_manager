from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionFindObject(Action):
    def name(self):
        return "action_find_object"

    def run(self, dispatcher, tracker, domain):

        object = tracker.get_slot("object")
        # Example: Detect object and set its location
        location = "table"
        direction = "left"
        distance = "a few feet"

        events = [
            SlotSet("object", object),
            SlotSet("object_distance", distance),
            SlotSet("object_direction", direction),
            SlotSet("object_location", location)
        ]

        # Respond to the user with the object location details
        response_text = f"I found the {object}. It's about {distance} meters away to the {direction}, located {location}."
        dispatcher.utter_message(text=response_text)

        return events

