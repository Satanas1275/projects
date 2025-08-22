import discord
from discord.ext import commands
import subprocess

TOKEN = "MTQwNjcwMjQzOTM2MDYyNjY5OA.GoiVDF.0m2T9VEuckR7slNOtdLuhrJ0hEi4tJ5_5douSM"

# ✅ Liste des utilisateurs autorisés
AUTHORIZED_USERS = [
    1103192768341352520,  # Ton ID
    1382505228187992147,  # Un autre ID
]

# ⚠️ IMPORTANT : il faut activer l'intent message_content
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.command()
async def cmd(ctx, *, command: str):
    if ctx.author.id not in AUTHORIZED_USERS:
        await ctx.send("⛔ Tu n'as pas la permission.")
        return

    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        output = result.stdout if result.stdout else result.stderr
        if not output:
            output = "✅ Commande exécutée sans sortie."
        await ctx.send(f"```\n{output[:1900]}\n```")  # Discord limite à 2000 caractères
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

bot.run(TOKEN)
