# ByteGuard

Discord Security Bot that prevents priviliged people from destroying the server

### Prerequisites

1. Discord Server
2. Discord Bot / Token 
    - **Scopes**
        - [x] `guilds` 
        - [x] `bot`
    - **Intents** 
        - [x] Server Members 
        - [x] Message Content
3. Python3.9 or higher


**.env**
```init
DISCORD_TOKEN=[Discord Bot Token]
CHANNEL_ID=[Admin Channel ID]
TIMESPAN=[Timespan for the removal reset]
REMOVALS=[Amount of allowed removals within the timespan]
```
