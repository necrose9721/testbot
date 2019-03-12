import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import pycparser

Client = discord.Client()
client = Bot(command_prefix="!")


@client.event
async def on_ready():
    print ("Le bot est pret et s'est connecté à discord !")

@client.event
async def on_member_join(member : discord.Member):
    points = open("Users/{},{}.txt".format(member.id, member.name), "w")
    points.write(str(50))
    points.close()
    
@client.event
async def on_message(message) :
    User = message.author.name
    UserID = message.author.id
    UserStatus = message.author.status
    UserJoin = message.author.joined_at
    UserMention = message.author.mention
    UserChannel = message.author.voice_channel
#commande pour jouer au lancé de dés
    if message.content.upper() == "!DES" :
        await client.send_message(message.channel,"Les dés roulent...")
        result = str(random.randint(1, 6))
        await client.send_message(message.channel,"Tu as fais : " + result)
        result = eval(result)
        if result == 6 and result > 5:
            await client.send_message(message.channel,"Tu gagne 4 points !")
            points = open("Users/{},{}.txt".format(UserID, User), "r")
            score = points.readline()
            points.close()
            score  = eval(score)+4
            points = open("Users/{},{}.txt".format(UserID, User), "w")
            points.write(str(score))
            points.close()
        if result <= 5 and result > 3:
            points = open("Users/{},{}.txt".format(UserID, User), "r")
            score = points.readline()
            points.close()
            await client.send_message(message.channel,"Tu gagne 2 points !")
            score  = eval(score)+2
            points = open("Users/{},{}.txt".format(UserID, User), "w")
            points.write(str(score))
            points.close()
        if result <= 3 and result > 1:
            points = open("Users/{},{}.txt".format(UserID, User), "r")
            score = points.readline()
            points.close()
            await client.send_message(message.channel,"Tu as perdu 1 point !")
            score  = eval(score)-1
            points = open("Users/{},{}.txt".format(UserID, User), "w")
            points.write(str(score))
            points.close()
        if result == 1:
            points = open("Users/{},{}.txt".format(UserID, User), "r")
            score = points.readline()
            points.close()
            await client.send_message(message.channel,"Tu as perdu 2 points !")
            score  = eval(score)-2
            points = open("Users/{},{}.txt".format(UserID, User), "w")
            points.write(str(score))
            points.close()
    #Regle
    if message.content.upper() == "!DESREGLES" :
        await client.send_message(message.channel,"Tu faire un lancé de dés en tapant !des.")
        await client.send_message(message.channel,"Si tu fait 1, tu perds 2 points ! :arrow_down: :two:")
        await client.send_message(message.channel,"Si tu fait 2 ou 3, tu perds 1 points ! :arrow_down: :one:")
        await client.send_message(message.channel,"Si tu fait 4 ou 5, tu gagnes 2 points ! :arrow_up: :two:")
        await client.send_message(message.channel,"Si tu fait 6, tu gagnes 4 points ! :arrow_up: :four:")
#Commande pour voir ses points
    if message.content.upper() == "!POINTS" :
        read = open("Users/{},{}.txt".format(UserID, User), "r", encoding="utf-8")
        points = read.readline()
        await client.send_message(message.channel, "%s Tu possèdes "%(UserMention) + points + " points !")
        read.close()
#Commande pour mettre un role
    if message.content.upper() == "!ADMIN" :
            user = message.author
            role = discord.utils.get(user.server.roles, name="Le PCiste Noir")
            await client.add_roles(user, role)
#Commande pour infos
    if message.content.upper() == "!INFOS" :
        await client.send_message(message.channel, "{}".format(UserMention))
        emb_infos = (discord.Embed(color=0x007F7F7F))
        emb_infos.set_author(name="Tes Informations : ", icon_url="http://millingtonlibrary.info/wp-content/uploads/2015/02/Info-I-Logo.png")
        emb_infos.add_field(name="Nom :", value=User)
        emb_infos.add_field(name="ID :", value=UserID)
        emb_infos.add_field(name="Status :", value=UserStatus)
        emb_infos.add_field(name="Arrivé le :", value=UserJoin)
        await client.send_message(message.channel, embed=emb_infos)
#Commande pour voir toute les commandes disponnibles
    if message.content.upper() == "!HELP" :
        emb_help = (discord.Embed(color=0x00FF7F7F))
        emb_help.set_author(name="Liste des commande disponible :", icon_url="http://is5.mzstatic.com/image/thumb/Purple128/v4/f9/12/88/f912886c-2592-5a9d-8cd2-2dde0ea117bf/source/256x256bb.png")
        emb_help.add_field(name="!des", value="Te permet de lancé les dès, tu peux aussi taper !desregles pour en savoir plus sur le jeu :game_die:")
        emb_help.add_field(name="!points", value="Te permet de voir le nombre de points que tu possèdes :keycap_ten:")
        emb_help.add_field(name="!infos", value="Te permet de voir tes information :writing_hand:")
        emb_help.add_field(name="!pf", value="Te permet de connaitre les commandes du pile ou face !")
        await client.send_message(message.channel, embed=emb_help)
#Commande pour pile ou face
    #Pour misé pile
    if message.content.upper().startswith("!PI") :
        if message.content.upper() == "!PI":
            await client.send_message(message.channel,"Tu dois mettre une mise !")
        else :
            piece = random.randint(1,2)
            pari = (message.content[4:])
            try:
                pari = int(pari)
                points = open("Users/{},{}.txt".format(UserID, User), "r")
                score = points.readline()
                points.close()
                print (piece)
                if piece > 1:
                    await client.send_message(message.channel,"La pièce retombe... Et...")
                    await client.send_message(message.channel,"C'est pile ! Tu gagne {} points :money_mouth: !".format(pari))
                    points = open("Users/{},{}.txt".format(UserID, User), "r")
                    score = points.readline()
                    points.close()
                    pari  = eval(score)+ pari
                    points = open("Users/{},{}.txt".format(UserID, User), "w")
                    points.write(str(pari))
                    points.close()
                    
                else:
                    await client.send_message(message.channel,"La pièce retombe... Et...")
                    await client.send_message(message.channel,"C'est face ! Tu perds {} points :confused: !".format(pari))
                    points = open("Users/{},{}.txt".format(UserID, User), "r")
                    score = points.readline()
                    points.close()
                    pari  = eval(score) - pari
                    points = open("Users/{},{}.txt".format(UserID, User), "w")
                    points.write(str(pari))
                    points.close()

            except ValueError:
                await client.send_message(message.channel,"Pour miser, c'est mieux des chiffres :D")
    #Pour misé face
    if message.content.upper().startswith("!FA") :
        if message.content.upper() == "!FA":
            await client.send_message(message.channel,"Tu dois mettre une mise !")
        else :
            piece = random.randint(1,2)
            pari = (message.content[4:])
            try:
                pari = int(pari)
                print (piece)
                if piece < 2 :
                    await client.send_message(message.channel,"La pièce retombe... Et...")
                    await client.send_message(message.channel,"C'est face ! Tu gagne {} points :money_mouth: !".format(pari))
                    points = open("Users/{},{}.txt".format(UserID, User), "r")
                    score = points.readline()
                    points.close()
                    pari  = eval(score)+ pari
                    points = open("Users/{},{}.txt".format(UserID, User), "w")
                    points.write(str(pari))
                    points.close()
                else:
                    await client.send_message(message.channel,"La pièce retombe... Et...")
                    await client.send_message(message.channel,"C'est pile ! Tu perds {} points :confused: !".format(pari))
                    points = open("Users/{},{}.txt".format(UserID, User), "r")
                    score = points.readline()
                    points.close()
                    pari  = eval(score) - pari
                    points = open("Users/{},{}.txt".format(UserID, User), "w")
                    points.write(str(pari))
                    points.close()

            except ValueError:
                await client.send_message(message.channel,"Pour miser, c'est mieux des chiffres :D")

    #regles
    if message.content.upper() == "!PF" :
        await client.send_message(message.channel,"Il existe 2 commandes :")
        await client.send_message(message.channel,"Tape !pi + 'mise' pour parier que la pièce va tombé sur pile")
        await client.send_message(message.channel,"Tape !fa + 'mise' pour parier que la pièce va tombé sur face")
        await client.send_message(message.channel,"Si tu gagnes, tu remportes autant de points que ta mise, si tu perds ta mise serra décomptée de tes points ! ")


client.run('')
