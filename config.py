#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    #APP_ID = os.environ.get("MicrosoftAppId", "23115394-d221-405d-8486-a217e747175c")
    #APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "n6B3.8~6_p7rjihQHPXR4oFUHgv08-aDkJ")
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "2cea84e9-2469-4066-96f7-6f7380b40067")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "80d13dff2572498dac3e4293ec3e16ec")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "bot-luis-service-authoring.cognitiveservices.azure.com/")
    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "1000412e-e221-4fa4-8f2a-26a1ca66825f")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "3f03349c-e125-4620-9f8c-9d16c6899f05")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://insurance-bot-qna-service.azurewebsites.net/qnamaker")