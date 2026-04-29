@client.on(events.NewMessage)
async def log_all(e):
    logging.info(f"{e.sender_id}: {e.text}")