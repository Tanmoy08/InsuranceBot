from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, PromptValidatorContext
from botbuilder.core import MessageFactory, TurnContext, UserState, CardFactory
from botbuilder.schema import InputHints, Attachment, ThumbnailCard, CardImage, Activity, ActivityTypes
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from config import DefaultConfig

from LUISRecognizer import InsuranceQueryRecognizer
from dataModels import UserData, InsuranceDetails
from helpers.luis_helper import LuisHelper, Intent
from dialogs import CancelHelpDialog

import os

from datetime import datetime
from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime

date = "date"
time = "time"

class ReservationBookingDialog(CancelHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(ReservationBookingDialog, self).__init__(dialog_id or ReservationBookingDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(TextPrompt(date, ReservationBookingDialog.datetime_prompt_validator))
        self.add_dialog(TextPrompt(time, ReservationBookingDialog.datetime_prompt_validator))
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
        else:
            return await step_context.prompt(
                date,
                PromptOptions(
                    prompt=MessageFactory.text("Please provide preferable date."),
                    retry_prompt=MessageFactory.text(
                        "Enter a valid date."
                    ),
                ),
            )        
        '''message_text = "Please provide preferable date"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))'''

    async def check_query_time(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["Date"] = step_context.result
        if(step_context.options.time != None):
            step_context.values["Time"] = step_context.options.time
            return await step_context.next(None)

        return await step_context.prompt(
            time,
            PromptOptions(
                prompt=MessageFactory.text("Please provide preferable time."),
                retry_prompt=MessageFactory.text(
                    "Enter a valid time."
                ),
            ),
        )  
        '''message_text = "Please provide preferable Time"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))'''

    async def summarize(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["Time"] = step_context.result

        message = Activity(type = ActivityTypes.message, attachments=[self.create_thumbnail_card(step_context)])
        await step_context.context.send_activity(message)
        return await step_context.end_dialog()

    def create_thumbnail_card(self, step_context: WaterfallStepContext) -> Attachment:
        card = ThumbnailCard(
            title = "Reservation Confirmed",
            text = "Kudos!! A reservation has been made at " + step_context.values["Location"] + " branch on " + step_context.values["Date"] + " at " + step_context.values["Time"],
            images=[
                CardImage(
                    url= "https://www.freepngimg.com/thumb/green_tick/27894-7-green-tick-transparent-background.png"
                    )
                ],
            ) 
        return CardFactory.thumbnail_card(card)

    @staticmethod
    async def datetime_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        is_valid = False
        results = recognize_datetime(prompt_context.recognized.value, Culture.English)
        for result in results:
            for resolution in result.resolution["values"]:
                if "value" in resolution:                    
                    value = resolution["value"]
                    if resolution["type"] == "date":
                        candidate = datetime.strptime(value, "%Y-%m-%d")
                        is_valid = True
                    elif resolution["type"] == "time":
                        candidate = datetime.strptime(value, "%H:%M:%S")
                        is_valid = True
                    else:
                        candidate = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")  
                        is_valid = True

        ret = prompt_context.recognized.succeeded and is_valid

        return ret

