#From https://youtu.be/Pa6T4ccloqo

from pypresence import Presence 
import time

start = int(time.time())
client_id = "" #your application's client id
RPC = Presence(client_id)
RPC.connect()

while True: #infinite loop
    RPC.update(
        large_image = "digiwind", #name of your asset
        large_text = "this is the digiwind logo",
        details = "thinking...",
        state = "Visual Studio Code",
        start = start,
        buttons = [{"label": "Digiwind on YouTube", "url": "https://www.youtube.com/channel/UCA-UkWyXFOrHiVvB9JfJEbw"}, {"label": "Discord", "url": "https://discord.gg/M6eFU3HrUn"}] #up to 2 buttons
    )
    time.sleep(60) #can be as low as 15, depends on how often you want to update
