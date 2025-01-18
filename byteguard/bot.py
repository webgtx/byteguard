import discord
from os import environ
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import environ

load_dotenv()

intents = discord.Intents.default() 
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
moderators_removals = dict()
channel_id = int(environ["CHANNEL_ID"])
timespan = int(environ["TIMESPAN"])
removals_allowed = int(environ["REMOVALS"])

@client.event
async def on_ready():
    print(f"We're logged in as {client.user}'")

@client.event
async def on_message(message):
    if message.author == client.user:
        return None

@client.event
async def on_member_remove(member):
    if member.guild.me.guild_permissions.view_audit_log:
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                moderator = entry.user
                await handle_kick_ban(member.guild, member, moderator, "kicked")
                return
        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target.id == member.id:
                moderator = entry.user
                await handle_kick_ban(member.guild, member, moderator, "banned")
                return

async def handle_kick_ban(guild, user, moderator, action):
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(f"{user.mention} has been {action} from {guild} by {moderator.mention}")
    else:
        print(f"Channel {channel_id} not found")

    if guild.id not in moderators_removals:
        moderators_removals[guild.id] = dict() 
    if moderator.id not in moderators_removals[guild.id]:
        moderators_removals[guild.id][moderator.id] = list()
    
    mod_journal = moderators_removals[guild.id][moderator.id]
    mod_journal.append(datetime.now())
    
    latest_removals = await fetch_latest_removals(timespan, mod_journal) 
    if len(latest_removals) >= removals_allowed: 
        await unroll_moderator(moderator)

    mod_journal = await fetch_latest_removals(10, mod_journal)

async def fetch_latest_removals(timespan: int, moderator_removal_history: dict):
    return [removal for removal in moderator_removal_history if removal > datetime.now() - timedelta(minutes=timespan)] 

async def unroll_moderator(moderator):
    channel = client.get_channel(channel_id)
    for role in moderator.roles:
        if role.name != "@everyone":
            try:
                await moderator.remove_roles(role)
            except discord.Forbidden:
                await channel.send(f"Couldn't unroll {moderator.mention} for excessive removals. **Missing permissions**")
    if channel:
        await channel.send(f"{moderator.mention} has been unrolled for excessive removals")
    else:
        print(f"Channel {channel_id} not found")
