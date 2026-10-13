import fluxer

intents = fluxer.Intents.default()
intents.MESSAGE_CONTENT = True

bot = fluxer.Bot(command_prefix="!", intents=intents)
