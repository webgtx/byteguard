from byteguard.bot import client
from os import environ

def main():
    client.run(environ["DISCORD_TOKEN"])
    
     
