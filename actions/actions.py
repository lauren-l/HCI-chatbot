from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from py_edamam import Edamam

ALLOWED_DIET_TYPES = ["no", "alcohol-free", "balanced", "high-fiber", "high-protein", "keto", "kosher", "low-carb", "low-fat", "low-sodium", "no-sugar", "paleo", "pescatarian", "pork-free", "vegan", "vegetarian"]

class ValidateRecipeaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_recipe_form"

    def validate_ingredients(
        self,
        slot_value: List,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `ingredients` value."""


        dispatcher.utter_message(text=f"OK! You have these ingredients: {', '.join(slot_value)}")
        return {"ingredients": slot_value}

    def validate_diet_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `diet_type` value."""

        diet = str(slot_value).lower()

        if diet not in ALLOWED_DIET_TYPES:
            dispatcher.utter_message(text=f"I don't recognize that diet. We serve {'/'.join(ALLOWED_DIET_TYPES)}.")
            return {"diet_type": None}
        elif diet == "no":
            dispatcher.utter_message(text=f"OK! You do not follow a specific diet.")
            return {"diet_type": diet}
        dispatcher.utter_message(text=f"OK! You follow a {diet} diet.")
        return {"diet_type": diet}

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
        ingredients = tracker.get_slot("ingredients")
        diet = tracker.get_slot("diet_type")

        message = "Try these recipes:\n" # message for bot to utter
        
        # form query
        if diet == "no":
            query = " ".join(ingredients)
        else:
            query = diet + " " + " ".join(ingredients)

        # query Edamam API
        query_result = e.search_recipe(query)['hits']
        if query_result == None:
            dispatcher.utter_message(text = "I couldn't find any recipes with the given criteria")
        else:
            for i, recipe in enumerate(query_result):
                message += f"Recipe {i+1}: {recipe['recipe']['label']}\n\tlink: {recipe['recipe']['url']}\n"
                if i == 5:
                    break
    
        dispatcher.utter_message(text = message)
        
        return []