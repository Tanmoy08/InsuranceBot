from botbuilder.schema import ActivityTypes, InputHints
from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    ComponentDialog,
    DialogContext,
    DialogTurnResult,
    DialogTurnStatus,
)

class CancelHelpDialog(ComponentDialog):
    def __init__(self, dialog_id: str):
        super(CancelHelpDialog, self).__init__(dialog_id)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        result = await self.interrupt(inner_dc)
        if result is not None:
            return result

        return await super(CancelHelpDialog, self).on_continue_dialog(inner_dc)

    async def interrupt(self, inner_dc: DialogContext) -> DialogTurnResult:
        if inner_dc.context.activity.type == ActivityTypes.message:
            text = inner_dc.context.activity.text.lower()

            help_message_text = "Show Help..."
            help_message = MessageFactory.text(
                help_message_text, help_message_text, InputHints.expecting_input
            )

            if text in ("help", "?"):
                await inner_dc.context.send_activity(help_message)
                await inner_dc.reprompt_dialog()
                return DialogTurnResult(DialogTurnStatus.Waiting)

            cancel_message_text = "Cancelling"
            cancel_message = MessageFactory.text(
                cancel_message_text, cancel_message_text, InputHints.ignoring_input
            )

            if text in ("cancel", "quit"):
                await inner_dc.context.send_activity(cancel_message)
                return await inner_dc.cancel_all_dialogs()

        return None