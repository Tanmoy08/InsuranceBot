from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext, UserState, CardFactory
from botbuilder.schema import InputHints, Attachment, ThumbnailCard, CardImage, Activity, ActivityTypes
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from config import DefaultConfig

from LUISRecognizer import InsuranceQueryRecognizer
from dataModels import UserData, InsuranceDetails
from helpers.luis_helper import LuisHelper, Intent
from dialogs import CancelHelpDialog

import os

class ReservationBookingDialog(CancelHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(ReservationBookingDialog, self).__init__(dialog_id or ReservationBookingDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.check_query_location,
                    self.check_query_date,
                    self.check_query_time,
                    self.summarize
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def check_query_location(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.options.location != None):
            step_context.values["Location"] = step_context.options.location
            return await step_context.next(None)
        message_text = "Please provide location"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def check_query_date(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["Location"] = step_context.result
        if(step_context.options.date != None):
            step_context.values["Date"] = step_context.options.date
            return await step_context.next(None)
        message_text = "Please provide preferable date"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def check_query_time(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["Date"] = step_context.result
        if(step_context.options.time != None):
            step_context.values["Time"] = step_context.options.time
            return await step_context.next(None)
        message_text = "Please provide preferable Time"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))

    async def summarize(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["Time"] = step_context.result
        #message = "Kudos!! A reservation has been made at " +  step_context.values["Location"] + " branch on " + step_context.values["Date"] + " at " + step_context.values["Time"]
        message = Activity(type = ActivityTypes.message, attachments=[self.create_thumbnail_card(step_context)])
        await step_context.context.send_activity(message)
        return await step_context.end_dialog()

    def create_thumbnail_card(self, step_context: WaterfallStepContext) -> Attachment:
        card = ThumbnailCard(
            title="Reservation Comfirmed",
            subtitle= "Kudos!! A reservation has been made at " + step_context.values["Location"] + " branch on " + step_context.values["Date"] + " at " + step_context.values["Time"],
            images=[
                CardImage(
                    url= os.path.join(os.getcwd(), "resources//Images//BookingConfirmed.png")
                    )
                ],
            ) 
        return CardFactory.thumbnail_card(card)