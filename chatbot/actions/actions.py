# This files contains your custom actions which can be used to run
# custom Python code.
#
from typing import Text, List, Any, Dict
from py_edamam import Edamam

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

ALLOWED_INGREDIENTS = []
ALLOWED_COOK_TIMES = ["15", "15 min", "15 minutes", "30", "30 min", "30 minutes", "1", "1 hr", "1 hour", ">1", ">1 hr", ">1hr", "> 1hr", "> 1 hr", ">1 hour", ">1hour", "> 1hour", "> 1 hour", "more than an hour", "more than 1 hour", "2hr", "2hrs", "2 hrs", "2 hours"]
ALLOWED_DIETARY_TYPES = ["vegetarian", "vegan", "non-vegetarian", "non-vegan", "meat eater", "no"]

class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_recipe_form"

    def validate_ingredients(
        self,
        slot_value: List,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, List]:
        """Validate `ingredients` value."""

        if slot_value.lower() not in ALLOWED_INGREDIENTS:
            dispatcher.utter_message(text=f"Sorry some of the ingredients are not supported. These are the possible inputs: {'/'.join(ALLOWED_COOK_TIMES)}")
            return {"ingredients": None}
        dispatcher.utter_message(text=f"OK! These are the ingredients you have: {slot_value}")
        return {"ingredients": slot_value}

    def validate_cook_times(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `cook_time` value."""

        if slot_value.lower() not in ALLOWED_COOK_TIMES:
            dispatcher.utter_message(text=f"I can only provide you with recipes for the following time durations: 15 min/30 min/1 hr/> 1 hr. These are the possible inputs: {'/'.join(ALLOWED_COOK_TIMES)}")
            return {"cook_time": None}
        dispatcher.utter_message(text=f"OK! You have {slot_value} to make a recipe.")
        return {"cook_time": slot_value}

    def validate_dietary_restriction(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `dietary_type` value."""

        if slot_value not in ALLOWED_DIETARY_TYPES:
            dispatcher.utter_message(text=f"Sorry, I can only suggest recipes for vegetarian, vegan or meat-based diets. Here are the possible inputs: {'/'.join(ALLOWED_DIETARY_TYPES)}.")
            return {"dietary_type": None}
        if slot_value is "no":
            dispatcher.utter_message(text=f"OK! You so you eat meat.")
        else:
            dispatcher.utter_message(text=f"OK! You are a {slot_value}.")
        return {"dietary_type": slot_value}

class ActionRecipeSearch(Action):
    def name(self) -> Text:
        return "action_recipe_search"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        """Search for recipe with matching criteria"""

        e = Edamam(recipes_appid="bf39108a", recipes_appkey='411d5b6d03551c704f48d3431162d55e')
        
        # get inputted ingredients + diet info from tracker
        ingredients = tracker.get_slot('ingredients')
        diet = tracker.get_slot('dietary_type')

        message = "Try these recipes:\n" # message for bot to utter
        
        # form query
        query = diet + " " + ingredients

        # query Edamam API
        query_result = e.search_recipe(query)
        if query_result == None:
            dispatcher.utter_message(text = "I couldn't find any recipes with the given criteria")
        else:
            for i, recipe in enumerate(query_result):
                message += f"Recipe {i}: {recipe.label}\t link: {recipe.url}\n"
                if i == 5:
                    break
    
        dispatcher.utter_message(text = message)
        
        return []