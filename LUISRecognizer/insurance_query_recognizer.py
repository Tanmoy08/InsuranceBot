from botbuilder.ai.luis import LuisApplication, LuisRecognizer
from botbuilder.core import Recognizer, RecognizerResult, TurnContext

from config import DefaultConfig

class InsuranceQueryRecognizer(Recognizer):
    def __init__(self, configuration: DefaultConfig):
        self._recognizer = None

        luis_is_configured = (
            configuration.LUIS_APP_ID,
            configuration.LUIS_API_KEY,
            configuration.LUIS_API_HOST_NAME
            )

        if luis_is_configured:
            luis_application = LuisApplication(
                configuration.LUIS_APP_ID,
                configuration.LUIS_API_KEY,
                "https://" + configuration.LUIS_API_HOST_NAME,
                )

        self._recognizer = LuisRecognizer(luis_application)

    @property
    def is_configured(self) -> bool:
        return self._recognizer is not None

    async def recognize(self, turn_context: TurnContext) -> RecognizerResult:
        return await self._recognizer.recognize(turn_context)