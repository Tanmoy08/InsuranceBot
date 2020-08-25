from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, NumberPrompt, PromptValidatorContext
from botbuilder.core import MessageFactory, TurnContext, UserState, CardFactory
from botbuilder.schema import InputHints, Activity, ActivityTypes, Attachment, ThumbnailCard, CardImage
from botbuilder.ai.qna import QnAMaker, QnAMakerEndpoint
from config import DefaultConfig
import os

from LUISRecognizer import InsuranceQueryRecognizer
from dataModels import UserData, InsuranceDetails
from helpers.luis_helper import LuisHelper, Intent

import re
from datetime import datetime
from recognizers_number import recognize_number, Culture
from recognizers_date_time import recognize_datetime

phone = "phone"
date = "date"

class InsuranceRenewalDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(InsuranceRenewalDialog, self).__init__(dialog_id or InsuranceRenewalDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__, InsuranceRenewalDialog.policynumber_prompt_validator))    
        self.add_dialog(TextPrompt(phone, InsuranceRenewalDialog.phone_prompt_validator))
        self.add_dialog(TextPrompt(date, InsuranceRenewalDialog.date_prompt_validator))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__, InsuranceRenewalDialog.phone_prompt_validator))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.check_query_policy_number,
                    self.check_query_mobile_number,
                    self.check_query_date_of_birth,                    
                    self.summarize
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def check_query_policy_number(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.options.policy_number != None):
            step_context.values["PolicyNumber"] = step_context.options.policy_number
            return await step_context.next(None)
         
        else:
            return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please provide your policy number."),
                        retry_prompt=MessageFactory.text(
                            "Enter a valid policy number."
                        ),
                    ),
                )
        '''message_text = "Please provide your policy number"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))'''

    async def check_query_mobile_number(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["PolicyNumber"] = step_context.result
        if(step_context.options.mobile_number != None):
            step_context.values["MobileNumber"] = step_context.options.mobile_number
            return await step_context.next(None)
        else:
            return await step_context.prompt(
                    phone,
                    PromptOptions(
                        prompt=MessageFactory.text("Please provide your phone number."),
                        retry_prompt=MessageFactory.text(
                            "Enter a valid phone number."
                        ),
                    ),
                )

        '''message_text = "Please provide your mobile number"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))'''

    async def check_query_date_of_birth(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["MobileNumber"] = step_context.result
        if(step_context.options.date_of_birth != None):
            step_context.values["DateOfBirth"] = step_context.options.date_of_birth
            return await step_context.next(None)
        else:
            return await step_context.prompt(
                date,
                PromptOptions(
                    prompt=MessageFactory.text("Please provide your date of birth."),
                    retry_prompt=MessageFactory.text(
                        "Enter a valid date of birth."
                    ),
                ),
            )
        '''message_text = "Please provide your Date of Birth"
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        return await step_context.prompt(date, PromptOptions(prompt=prompt_message))'''


    async def summarize(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if(step_context.result != None):
            step_context.values["DateOfBirth"] = step_context.result
        message = Activity(type = ActivityTypes.message, attachments=[self.create_thumbnail_card(step_context)])
        '''message = "Your Policy Number: " +  step_context.values["PolicyNumber"] + " has been renewed. New Policy number and details will be messaged to " + step_context.values["MobileNumber"]'''
        await step_context.context.send_activity(message)
        return await step_context.end_dialog()

    def create_thumbnail_card(self, step_context: WaterfallStepContext) -> Attachment:
        card = ThumbnailCard(
            title="Insurance Renewed",
            subtitle= "Your Policy Number: " +  step_context.values["PolicyNumber"] + " has been renewed. New Policy number and details will be messaged to " + step_context.values["MobileNumber"],
            images=[
                CardImage(
                    url= os.path.join(os.getcwd(), "resources//Images//BookingConfirmed.png")
                    )
                ],
            ) 
        return CardFactory.thumbnail_card(card)

    @staticmethod
    async def age_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        # This condition is our validation rule. You can also change the value at this point.
        return (
            prompt_context.recognized.succeeded
            and 0 < prompt_context.recognized.value < 150
        )

    @staticmethod
    async def policynumber_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        ret = prompt_context.recognized.succeeded and re.match("[A-Za-z]{2}[0-9]{6}[A-Za-z]", prompt_context.recognized.value)   
        return ret

    @staticmethod
    async def phone_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        ret = prompt_context.recognized.succeeded and re.match("[0-9]{10}", prompt_context.recognized.value)
        return ret

    @staticmethod
    async def date_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        is_valid = False
        results = recognize_datetime(prompt_context.recognized.value, Culture.English)
        for result in results:
            for resolution in result.resolution["values"]:
                if "value" in resolution:
                    
                    value = resolution["value"]
                    if resolution["type"] == "date":
                        candidate = datetime.strptime(value, "%Y-%m-%d")
                        is_valid = True

        ret = prompt_context.recognized.succeeded and is_valid

        return ret
    


            
