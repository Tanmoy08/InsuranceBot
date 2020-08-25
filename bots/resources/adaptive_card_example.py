
ADAPTIVE_CARD_CONTENT = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.0",
    "type": "AdaptiveCard",
    "speak": "Insurance Services Welcome Page",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
               {
                   "type": "Column",
                   "width": 2,
                   "items": [
                      {
                          "type": "TextBlock",
                          "text": "InSure",
                          "weight": "bolder",
                          "size": "extraLarge",
                          "spacing": "none"
                      },
                      {
                          "type": "TextBlock",
                          "text": "Your Companion",
                          "size": "Large",
                          "spacing": "none"
                      },
                      {
                          "size": "small",
                          "text": "Hi! Welcome to InSure.Pvt.Ltd. \n My name is InSure and I am here to answer your queries, help you book an appointment and assist you in renewal of your existing insurance.",
                          "type": "TextBlock",
                          "wrap": "true"
                      }
                   ]
               },
               {
                  "type": "Column",
                  "width": 1,
                  "items": [
                    {
                      "size": "auto",
                      "type": "Image",
                      "url": "https://miro.medium.com/max/700/1*MAsNORFL89roPfIFMBnA4A.jpeg"
                    }
                  ]
               }
          ]
        }
    ],
    "actions": [
    {
      "type": "Action.OpenUrl",
      "title": "View our goals",
      "url": "https://www.google.co.in/"
    },
    {
      "type": "Action.OpenUrl",
      "title": "About Us",
      "url": "https://www.google.co.in/"
    }
  ],
}
