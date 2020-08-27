from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    ConversationState,
    CardFactory,
    MessageFactory
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes, 
    Attachment, 
    Activity, 
    ActivityTypes
)

import os
import json
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from dataModels import ConversationData


from resources.adaptive_card_welcome import ADAPTIVE_CARD_CONTENT


class InsuranceBot(ActivityHandler):
    def __init__(self, conversation_state: ConversationState, user_state: UserState, dialog: Dialog):
        if conversation_state is None:
            raise Exception("[DialogBot]: Missing parameter. conversation_state is required")
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

        self.conversation_data_accessor = self.conversation_state.create_property("ConversationData")
        self.user_profile_accessor = self.user_state.create_property("UserData")

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                message = Activity(type = ActivityTypes.message, attachments=[self.create_adaptive_card()],)
                await turn_context.send_activity(message)

                message_text = "what is your name?"
                await turn_context.send_activity(message_text)

    async def on_message_activity(self, turn_context: TurnContext):
        conversation_data = await self.conversation_data_accessor.get(turn_context, ConversationData)
        temp = conversation_data.data if conversation_data.data != None else []
        temp.append(turn_context.activity.text)
        conversation_data.data = temp[1:] if len(temp)>5 else temp

        await DialogHelper.run_dialog(self.dialog, turn_context,self.conversation_state.create_property("DialogState"))

    def create_adaptive_card(self) -> Attachment:
        return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)
