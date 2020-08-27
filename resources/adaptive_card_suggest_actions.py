
ADAPTIVE_CARD_SUGGEST_ACTIONS = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.0",
    "type": "AdaptiveCard",
    "speak": "Insurance Services Welcome Page",
    "body": [
        {
            "speak": "Insurance Services",
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                           "type": "TextBlock",
                           "text": "message",
                           "size": "Medium",
                           "spacing": "none",
                           "horizontalAlignment": "Left"
                        }
                    ]
                }
             ]
        }
    ],
    "actions": [
    {
      "type": "Action.Submit",
      "title": "What is Health Insurance?",
      "value": "What is Health Insurance?",
      "data": "What is Health Insurance?"
    },
    {
      "type": "Action.Submit",
      "title": "Book Appointment",
      "value": "Book Appointment",
      "data": "Book Appointment"
    },
    {
      "type": "Action.Submit",
      "title": "Insurance Renewal",
      "value": "Insurance Renewal",
      "data": "Insurance Renewal"
    }
  ],
}
