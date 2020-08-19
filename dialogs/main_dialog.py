from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, TurnContext, UserState, CardFactory
from botbuilder.schema import InputHints, CardAction, ActionTypes, Attachment, Activity, ActivityTypes
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from config import DefaultConfig

from LUISRecognizer import InsuranceQueryRecognizer
from dataModels import UserData, InsuranceDetails
from helpers.luis_helper import LuisHelper, Intent
from dialogs import InsuranceRenewalDialog, ReservationBookingDialog

CARDS = ["resources\\suggest_actions.json"]

import os
import json

INS_PROMPT_OPTIONS = "Insurance Services options"

config = DefaultConfig()

class MainDialog(ComponentDialog):
    def __init__(self, user_state: UserState, luis_recognizer: InsuranceQueryRecognizer,
                 insurance_renewal_dialog: InsuranceRenewalDialog, reservation_booking_dialog: ReservationBookingDialog):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.qna_maker = QnAMaker(
            QnAMakerEndpoint
            (
                knowledge_base_id=config.QNA_KNOWLEDGEBASE_ID,
                endpoint_key=config.QNA_ENDPOINT_KEY,
                host=config.QNA_ENDPOINT_HOST
                )
            )

        self.user_profile_accessor = user_state.create_property("UserData")
        self.insurance_renewal_dialog_id = insurance_renewal_dialog.id
        self.reservation_booking_dialog_id = reservation_booking_dialog.id
        self._luis_recognizer = luis_recognizer
        self.user_state = user_state
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(INS_PROMPT_OPTIONS))
        self.add_dialog(insurance_renewal_dialog)
        self.add_dialog(reservation_booking_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",[
                    self.intro_step,
                    self.name_process_step,
                    self.luis_query_step,
                    self.closing_step
                    ]
                )
            )
        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
       user_profile = await self.user_profile_accessor.get(step_context.context, UserData)
       if(user_profile.name != None):
           return await step_context.next(None)
       user_profile.name = step_context._turn_context._activity.text
       return await step_context.next(None)
       '''message_text = "what is your name?"
       prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
       return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))'''

    async def name_process_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_profile = await self.user_profile_accessor.get(step_context.context, UserData)
        if(user_profile.name != None and  user_profile.user_greeted == True):
            message_text = "What else can I do for you "+ user_profile.name + " ?"
        else:
            user_profile.user_greeted = True
            message_text = "Hi "+ user_profile.name+ ", How can I help you today?"
        message = Activity(type = ActivityTypes.message, attachments=[self._create_adaptive_card_attachment(message_text)],)
        '''prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)       
        await step_context.context.send_activity(message)'''
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=message))

    async def luis_query_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if not self._luis_recognizer.is_configured:
            message_text = "LUIS Not Configured"
            response = self.create_response(turn_context.activity, message_text)
            await turn_context.send_activity(response)
            message_text = "What can I help you with today?"
            await step_context.context.send_activity(MessageFactory.text(message_text))
            return await step_context.replace_dialog(self.id, message_text)

        intent, luis_result = await LuisHelper.execute_luis_query(self._luis_recognizer, step_context.context)

        if(intent == "Renewal_Of_Insurance"):
            '''message_text = "Yout Intent "+intent
            await step_context.context.send_activity(MessageFactory.text(message_text))'''
            return await step_context.begin_dialog(self.insurance_renewal_dialog_id, luis_result)
        elif intent == "Appointment_Booking":
            '''message_text = "Yout Intent "+intent
            await step_context.context.send_activity(MessageFactory.text(message_text))'''
            return await step_context.begin_dialog(self.reservation_booking_dialog_id, luis_result)
        else:
            response = await self.qna_maker.get_answers(step_context.context)
            if response and len(response) > 0: 
                await step_context.context.send_activity(MessageFactory.text(response[0].answer))
            else: 
                await step_context.context.send_activity("No QnA Maker answers were found.")
        return await step_context.next(None)

    async def closing_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.replace_dialog(self.id, None)

    def get_choices(self):
         insurance_services_options = [
             Choice(value="Health Insurance", synonyms=["Health Insurance", "*"]),
             Choice(value="Book an appointment", synonyms=["Book an appointment"]),
             Choice(value="Renew Insurance", synonyms=["Renew Insurance"]),
             ]
         return insurance_services_options

    def _create_adaptive_card_attachment(self, message: str = None) -> Attachment:
         card_path = os.path.join(os.getcwd(), CARDS[0])
         with open(card_path, "rb") as in_file:
             card_data = json.load(in_file)
             card_data['body'][0]['columns'][0]['items'][0]['text'] = message
         return CardFactory.adaptive_card(card_data)