from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker
from typing import Any, Dict, List, Text
import requests
from config import object_finder_config    
import time 
from rasa_sdk.events import Restarted


class ActionFindObject(Action):
    def name(self) -> Text:
        return "action_find_object"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        object_to_find = tracker.get_slot("object")
        url = object_finder_config['OF_API_URL']
       
         # start the detection server here 
        try:
            response= requests.post(f"{url}/set_target", json= {"target": object_to_find})
            response.raise_for_status()  # Raise an error for unsuccessful requests
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message("There was an error setting the target object  of the  object finder.")
        

        try:
            response= requests.post(f"{url}/start_pipelines")
            response.raise_for_status()  # Raise an error for unsuccessful requests
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message("There was an error statring the object finder")
    
        
        # response= requests.post(f"{url}/stop_pipelines")
        
        # If confirmed, proceed with object location guidance
        dispatcher.utter_message(
            text=f"Looking for the {object_to_find}. Move around slowly to help me locate it."
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
      

        return events
    
class ActionStopObjectFinder(Action):

    def name(self) -> str:
        return "action_stop_object_finder"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # The URL of the REST API endpoint you want to call
        url = object_finder_config['OF_API_URL']
        

        payload={}
        # Making the REST API call
        try:
            response = requests.post(f"{url}/stop_pipelines", json=payload)
            response.raise_for_status()  # Raise an error for unsuccessful requests
            dispatcher.utter_message("Object finder has been stopped.")
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message("There was an error stopping the object finder.")
            print(f"Error calling REST API: {e}")

        return []





from rasa_sdk import Action
from rasa_sdk.events import Restarted

class ActionIntroduceNova(Action):
    def name(self):
        return "action_restart_conversation_with_message"
    
    def run(self, dispatcher, tracker, domain):
        # Introduction message tailored for visually impaired users
        dispatcher.utter_message(text="Hello! I am Nova, your voice assistant. How can I assist you today? Feel free to ask for help with anything you need.")
        return [Restarted()]





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




