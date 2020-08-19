from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from dataModels import InsuranceDetails, BookingReservation

class Intent(Enum):
    BOOK_APPOINTMENT = "Appointment_Booking"
    NONE_INTENT = "None"
    RENEWAL_OF_INSURANCE = "Renewal_Of_Insurance"

def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)

class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
        ) -> (Intent, object):
        result = None
        intent = None
        insurance_detail = InsuranceDetails()
        reservation_booking_detail = BookingReservation()

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                    )[:1][0]
                if recognizer_result.intents
                else None
                )

            if intent == Intent.RENEWAL_OF_INSURANCE.value and recognizer_result.as_dict.__self__.intents[intent].score > 0.85:

                phone_entities = recognizer_result.entities.get("$instance", {}).get(
                    "India_Phone_Number", []
                )
                if len(phone_entities) > 0:
                    '''if recognizer_result.entities.get("India_Phone_Number", [{"$instance": {}}])[0]["$instance"]:'''
                    insurance_detail.mobile_number = phone_entities[0]["text"].capitalize()
                else:
                    insurance_detail.mobile_number = None

                date_entities = recognizer_result.entities.get("datetime", [])
                if date_entities:
                    '''if recognizer_result.entities.get("datetime", [{"$instance", {}}])[0]["$instance"]:'''
                    timex = date_entities[0]["timex"]
                    if timex:
                        insurance_detail.date_of_birth = timex[0].split("T")[0]
                else:
                    insurance_detail.date_of_birth = None

                insurance_number_entities = recognizer_result.entities.get("$instance", {}).get(
                    "Insurance_number", []
                    )
                if len(insurance_number_entities) > 0:
                    '''if recognizer_result.entities.get("Insurance_number", [{"$instance", {}}])[0]["$instance"]:'''
                    insurance_detail.policy_number = insurance_number_entities[0]["text"].capitalize()
                else:
                    insurance_detail.policy_number = None
                return intent, insurance_detail

            elif intent == Intent.BOOK_APPOINTMENT.value and recognizer_result.as_dict.__self__.intents[intent].score > 0.85:
                date_entities = recognizer_result.entities.get("datetime", [])
                if date_entities:
                    '''if recognizer_result.entities.get("datetime", [{"$instance", {}}])[0]["$instance"]:'''
                    timex = date_entities[0]["timex"]
                    if timex:
                        if timex[0].split("T")[0] != None and timex[0].split("T")[0] != "":
                            reservation_booking_detail.date = timex[0].split("T")[0]
                        else: reservation_booking_detail.date = None
                        if len(timex[0].split("T"))>1 and timex[0].split("T")[1] != None:
                            reservation_booking_detail.time = timex[0].split("T")[1]
                        else: reservation_booking_detail.time = None
                else:
                    reservation_booking_detail.date = None
                    reservation_booking_detail.time = None
                    
                location_entities = recognizer_result.entities.get("$instance", {}).get(
                    "Location", []
                )
                if len(location_entities) > 0:
                    '''if recognizer_result.entities.get("Location", [{"$instance": {}}])[0]["$instance"]:'''
                    reservation_booking_detail.location = location_entities[0]["text"].capitalize()
                else:
                    reservation_booking_detail.location = None
                return intent, reservation_booking_detail
            else:
                result = None
                intent = None
        except Exception as exception:
            print(exception)
        return intent, result