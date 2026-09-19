import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True  # Remember to turn this on in your Developer Portal!
bot = commands.Bot(command_prefix="?", intents=intents)

# Hardcoded collection of bots and their fixed gear sets
BOT_BOSSES = {
    "mee6": {"name": "MEE6", "hp": 100, "gear": "Legendary Leveling Shield & Golden Microphone", "attack": 12},
    "tatsu": {"name": "Tatsu", "hp": 120, "gear": "Mythic Daycare Sword & Pet Companion Armor", "attack": 10},
    "dankmemer": {"name": "Dank Memer", "hp": 90, "gear": "Enchanted Pepe Coin Shield & Hunting Rifle", "attack": 15}
}

# Temporary memory to track active fights
active_fights = {}

@bot.command()
async def fight(ctx, boss_name: str = None):
    if not boss_name:
        await ctx.send("❌ **Error:** Please specify a bot to fight! *Example: `?fight mee6`*")
        return
        
    boss_key = boss_name.lower().replace(" ", "")
    if boss_key not in BOT_BOSSES:
        await ctx.send(f"❌ Boss '{boss_name}' not found. Choose from: MEE6, Tatsu, DankMemer")
        return

    # Check if player is already in a fight
    if ctx.author.id in active_fights:
        await ctx.send("⚠️ You are already in an active battle! Use `?attack` to take your turn.")
        return

    boss_data = BOT_BOSSES[boss_key]
    
    # Initialize the current fight data
    active_fights[ctx.author.id] = {
        "boss_name": boss_data["name"],
        "boss_hp": boss_data["hp"],
        "boss_max_hp": boss_data["hp"],
        "boss_attack": boss_data["attack"],
        "boss_gear": boss_data["gear"],
        "player_hp": 100
    }

    embed = discord.Embed(title="⚔️ BATTLE INITIATED ⚔️", color=discord.Color.red())
    embed.add_field(name="Opponent", value=f"**{boss_data['name']}**", inline=True)
    embed.add_field(name="Set Gear Equipped", value=boss_data['gear'], inline=False)
    embed.add_field(name="Your HP", value="100 / 100", inline=True)
    embed.add_field(name="Enemy HP", value=f"{boss_data['hp']} / {boss_data['hp']}", inline=True)
    embed.set_footer(text="Type ?attack to strike your opponent!")
    
    await ctx.send(embed=embed)

@bot.command()
async def attack(ctx):
    if ctx.author.id not in active_fights:
        await ctx.send("❌ You are not in an active fight! Start one with `?fight [bot_name]`")
        return

    fight = active_fights[ctx.author.id]
    
    # Player attacks enemy
    player_damage = random.randint(15, 30)
    fight["boss_hp"] -= player_damage
    
    battle_log = f"💥 **{ctx.author.name}** dealt **{player_damage} damage** to {fight['boss_name']}!\n"

    # Check if enemy died
    if fight["boss_hp"] <= 0:
        await ctx.send(f"🏆 **VICTORY!** You successfully defeated **{fight['boss_name']}**!")
        del active_fights[ctx.author.id]
        return

    # Enemy counters and attacks player
    boss_damage = random.randint(5, fight["boss_attack"] + 5)
    fight["player_hp"] -= boss_damage
    battle_log += f"🛡️ **{fight['boss_name']}** counters using their *{fight['boss_gear']}*, dealing **{boss_damage} damage** back!\n"

    # Check if player died
    if fight["player_hp"] <= 0:
        await ctx.send(f"💀 **DEFEAT!** You were crushed by **{fight['boss_name']}**.")
        del active_fights[ctx.author.id]
        return

    # Display updated health pools
    embed = discord.Embed(title=f"🥊 Combat Turn Log", description=battle_log, color=discord.Color.blue())
    embed.add_field(name="Your HP", value=f"{fight['player_hp']} / 100", inline=True)
    embed.add_field(name=f"{fight['boss_name']} HP", value=f"{fight['boss_hp']} / {fight['boss_max_hp']}", inline=True)
    
    await ctx.send(embed=embed)

# Insert your actual Bot Token from the Discord Developer Portal here
bot.run("YOUR_BOT_TOKEN_HERE")
