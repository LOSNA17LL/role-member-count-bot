import sys, os, settings, discord
from dotenv import load_dotenv

#Initialisation
load_dotenv()
BOTTOKEN=os.getenv('BOTTOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
client = discord.Client(intents=intents)

#Support functions
def vc_name_from_role_name_and_number(rolename,n):
    return f"{rolename} : {n}"

def verify_role_is_followed(role_):
    server_ =role_.guild
    role_name=role_.name
    L_categories=server_.categories
    for cat in L_categories:
        cat_name=cat.name
        if cat_name=="--Server Stats--":
            for vchan in cat.voice_channels:
                if vchan.name.startswith(role_name):
                    return vchan
    return False
                


#Events
@client.event
async def on_ready():print(f'Logged on as {client.user}!')

@client.event
async def on_message(message):
    if message.content=="Ping":
        await message.channel.send("Pong")

@client.event
async def on_member_update(before,after):
    B_roles,A_roles=set(before.roles),set(after.roles)
    if B_roles==A_roles:return
    updrole=e = next(iter(B_roles^A_roles))#next(iter()) to get the only element of the set
    role_vchan=verify_role_is_followed(updrole)
    if role_vchan:
        newchanname=vc_name_from_role_name_and_number(updrole.name,len(updrole.members))
        print(newchanname)
        await role_vchan.edit(name=newchanname)
#Due to the limit of 2 voicechan edits / vchan / 10min, if needed to edit the vchan more than that... just wait 10min, more advanced stuff will come later

#Run
client.run(BOTTOKEN)