def extract_user_id(msg):
    if msg.reply_to_message:
        return msg.reply_to_message.from_user.id
    elif msg.command and len(msg.command) > 1 and msg.command[1].isdigit():
        return int(msg.command[1])
    return None
