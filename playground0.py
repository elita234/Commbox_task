text= '''CommBox (formerly BumpYard) was founded in 2013 by Eli Israelov and Yaniv Hakim to offer an innovative way for organizations to communicate with their customers. 

We at CommBox have developed an advanced AI-powered omnichannel customer communication platform that allows any organization to manage seamless communication with customers across channels: WhatsApp, Facebook Messenger, Instagram, chat, email, Google, SMS, video chat, and more, all in one smart inbox. 

CommBox is an official WhatsApp partner and is considered the pioneer in customer service automation. Hundreds of companies across sectors adopted the CommBox solution to offer their services to 50+ million customers worldwide.

Step forward to the next generation of digital customer communication with CommBox!'''

import openai
openai.api_key = 'key'

response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a professional assistant."},
        {"role": "system", "content": f"Answer the next question about the following text: '{text}'"},
        {"role": "user", "content": "When was Commbox founded?"}
  ]
)

print(response)