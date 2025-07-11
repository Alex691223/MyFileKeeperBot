services:
  - type: web
    name: tg-moderator-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: BOT_TOKEN
        value: 7152364773:AAHhlKTUfQcoYz5myyxYm1FoPpzU9j-q9vU
      - key: SUPERADMIN_ID
        value: "954426279"
