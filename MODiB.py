import os
import discord, random, json

#Innitialising game data.
Json = open('Crits_Fails_Attack.json', 'r')
Crits = json.load(Json)
Crit_Fails_Attack = list(Crits)
Json.close
Json = open('Crits_Success_Attack.json', 'r')
Crits = json.load(Json)
Crit_Success_Attack = list(Crits)
Json.close
Json = open('Crits_Fails_Defense.json', 'r')
Crits = json.load(Json)
Crit_Fails_Defense = list(Crits)
Json.close
Json = open('Crits_Success_Defense.json', 'r')
Crits = json.load(Json)
Crit_Success_Defense = list(Crits)
Json.close
Json = open('Spell_List.json', 'r')
Spells = json.load(Json)
Spell_List = list(Spells)
Json.close

#Innitialising properties of all characters.
Json = open('Properties_Taravan.json', 'r')
Properties = json.load(Json)
Property_List_Taravan = list(Properties)
Json.close

#Innitialising abilities of all characters.
Json = open('Abilities_Cloi.json', 'r')
Abilities = json.load(Json)
Ability_List_Cloi = list(Abilities)
Json.close
Json = open('Abilities_Cordovan.json', 'r')
Abilities = json.load(Json)
Ability_List_Cordovan = list(Abilities)
Json.close
Json = open('Abilities_Leonidas.json', 'r')
Abilities = json.load(Json)
Ability_List_Leonidas = list(Abilities)
Json.close
Json = open('Abilities_Taravan.json', 'r')
Abilities = json.load(Json)
Ability_List_Taravan = list(Abilities)
Json.close

#Innitialising spells of all characters.
# Json = open('Spells_Cloi.json', 'r')
# Spells = json.load(Json)
# Spell_List_Cloi = list(Spells)
# Json.close
# Json = open('Spells_Cordovan.json', 'r')
# Spells = json.load(Json)
# Spell_List_Cordovan = list(Spells)
# Json.close
Json = open('Spells_Taravan.json', 'r')
Spells = json.load(Json)
Spell_List_Taravan = list(Spells)
Json.close

#Innitialising weapons of all characters.
Json = open('Weapons_Cloi.json', 'r')
Weapons = json.load(Json)
Weapon_List_Cloi = list(Weapons)
Json.close
Json = open('Weapons_Cordovan.json', 'r')
Weapons = json.load(Json)
Weapon_List_Cordovan = list(Weapons)
Json.close
Json = open('Weapons_Leonidas.json', 'r')
Weapons = json.load(Json)
Weapon_List_Leonidas = list(Weapons)
Json.close
Json = open('Weapons_Taravan.json', 'r')
Weapons = json.load(Json)
Weapon_List_Taravan = list(Weapons)
Json.close

#Funktion that fixes the Umlaute problem
def umlaute(string):
    string = string.replace("ã¤", "ä")
    string = string.replace("Ã¤", "ä")
    string = string.replace("ã¼", "ü")
    string = string.replace("Ã¼", "ü")
    string = string.replace("ã¶", "ö")
    string = string.replace("Ã¶", "ö")
    string = string.replace("ÃŸ", "ß")
    string = string.replace("â€“", "–")
    return string

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

#Assigns correct weapons, abilities and stats to the current user based on Discord name of latest message author. Updated on every message.
    if str(message.author) == "Aelron#6030":
        Current_Attack_Set = Weapon_List_Cordovan
        Current_Ability_Set = Ability_List_Cordovan
    if str(message.author) == "Echtgeilman92#2052":
        Current_Attack_Set = Weapon_List_Cloi
        Current_Ability_Set = Ability_List_Cloi
    if str(message.author) == "Friedrich#6066" or str(message.author) == "Ponk#0213":
        Current_Attack_Set = Weapon_List_Taravan
        Current_Ability_Set = Ability_List_Taravan
        Current_Property_Set = Property_List_Taravan
        Current_Spell_List = Spell_List_Taravan
    if str(message.author) == "JohannesDberg#9702":
        Current_Attack_Set = Weapon_List_Leonidas
        Current_Ability_Set = Ability_List_Leonidas
        Current_Spell_List = []

#Command handling standard attack commands.
    if message.content.startswith('!Angriff') or message.content.startswith('!angriff'):
        Weapon = message.content[9:].lower()
        for i in range(len(Current_Attack_Set)):
            if umlaute(Weapon) == umlaute(Current_Attack_Set[i]["Name"].lower()):
                Roll = random.randint(1,20)
                Grundschaden = 0
                for j in range(int(Current_Attack_Set[i]["Schaden"])):
                    Grundschaden += random.randint(1,6)
                Schaden = Grundschaden + int(Current_Attack_Set[i]["Modifikator"])
                if Roll == 20:
                    Effekt = random.randint(1,100)
                    await message.channel.send("**Kritischer Erfolg!** Nebeneffekt: " + str(Effekt))
                    await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Schaden"] + "W6+" + Current_Attack_Set[i]["Modifikator"] + ")")
                    for i in range(len(Crit_Success_Attack)):
                        if int(Crit_Success_Attack[i]["Wert"]) <= Effekt:
                            Effekt_Ausgabe = Crit_Success_Attack[i]["Effekt"]
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                elif Roll == 1:
                    Effekt = random.randint(1,100)
                    await message.channel.send("**Kritischer Misserfolg!** Nebeneffekt: " + str(Effekt))
                    for i in range(len(Crit_Fails_Attack)):
                        if int(Crit_Fails_Attack[i]["Wert"]) <= Effekt:
                            Effekt_Ausgabe = Crit_Fails_Attack[i]["Effekt"]
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                else:
                    if Roll + int(Current_Attack_Set[i]["FF"]) < 20:
                        await message.channel.send("Kein Treffer " + "**" + str(Roll) + "**+" + Current_Attack_Set[i]["FF"] + "=" + str(Roll + int(Current_Attack_Set[i]["FF"])))
                    else:
                        await message.channel.send("Treffer " + "**" + str(Roll) + "**+" + Current_Attack_Set[i]["FF"] + "=" + str(Roll + int(Current_Attack_Set[i]["FF"])))
                        await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Schaden"] + "W6+" + Current_Attack_Set[i]["Modifikator"] + ")")

#Command handling skill checks.
    if message.content.startswith('!Test') or message.content.startswith('!test'):
        Ability = message.content[6:].lower()
        Roll = random.randint(1,20)
        if Ability == 'abwehr' and Roll == 1 or Ability == 'abwehr' and Roll == 20:
            if Roll == 1:
                Effekt = random.randint(1,100)
                await message.channel.send("**Kritischer Misserfolg!** Nebeneffekt: " + str(Effekt))
                for i in range(len(Crit_Fails_Defense)):
                    if int(Crit_Fails_Defense[i]["Wert"]) <= Effekt:
                        Effekt_Ausgabe = Crit_Fails_Defense[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            if Roll == 20:
                Effekt = random.randint(1,100)
                await message.channel.send("**Kritischer Erfolg!** Nebeneffekt: " + str(Effekt))
                for i in range(len(Crit_Success_Defense)):
                    if int(Crit_Success_Defense[i]["Wert"]) <= Effekt:
                        Effekt_Ausgabe = Crit_Success_Defense[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
        else:
            for i in range(len(Current_Ability_Set)):
                if Ability == umlaute(Current_Ability_Set[i]["Ability"].lower()):
                    if Roll == 20:
                        await message.channel.send("Kritischer Erfolg: " + "**" + str(Roll) + "**" + "+" + Current_Ability_Set[i]["Wert"] + "=" + str(Roll+int(Current_Ability_Set[i]["Wert"])))
                    elif Roll == 1:
                        await message.channel.send("Kritischer Misserfolg: " + "**" + str(Roll) + "**" + "+" + Current_Ability_Set[i]["Wert"] + "=" + str(Roll+int(Current_Ability_Set[i]["Wert"])))
                    else:
                        await message.channel.send("**" + str(Roll) + "**" + "+" + Current_Ability_Set[i]["Wert"] + "=" + str(Roll+int(Current_Ability_Set[i]["Wert"])))

#Command handling fencing attack commands.
    if message.content.startswith('!Fechtangriff') or message.content.startswith('!fechtangriff'):
        Weapon = message.content[14:].lower()
        Fencing_Value = str(int(Current_Ability_Set[15]["Wert"]) + int(Current_Property_Set[10]["Wert"]) + 2) ############!!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(len(Current_Attack_Set)):
            if umlaute(Weapon) == umlaute(Current_Attack_Set[i]["Name"].lower()):
                Roll = random.randint(1,20)
                Grundschaden = 0
                for j in range(int(Current_Attack_Set[i]["Schaden"])):
                    Grundschaden += random.randint(1,6)
                Schaden = Grundschaden + int(Current_Attack_Set[i]["Modifikator"]) - int(Current_Property_Set[9]["Wert"])
                if Roll == 20:
                    Effekt = random.randint(1,100)
                    await message.channel.send("**Kritischer Erfolg!** Nebeneffekt: " + str(Effekt))
                    await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Schaden"] + "W6+" + str(int(Current_Attack_Set[i]["Modifikator"]) - int(Current_Property_Set[9]["Wert"])) + ")")
                    for i in range(len(Crit_Success_Attack)):
                        if int(Crit_Success_Attack[i]["Wert"]) <= Effekt:
                            Effekt_Ausgabe = Crit_Success_Attack[i]["Effekt"]
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                elif Roll == 1:
                    Effekt = random.randint(1,100)
                    await message.channel.send("**Kritischer Misserfolg!** Nebeneffekt: " + str(Effekt))
                    for i in range(len(Crit_Fails_Attack)):
                        if int(Crit_Fails_Attack[i]["Wert"]) <= Effekt:
                            Effekt_Ausgabe = Crit_Fails_Attack[i]["Effekt"]
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                else:
                    if Roll + int(Fencing_Value) < 20:
                        await message.channel.send("Kein Treffer " + "**" + str(Roll) + "**+" + Fencing_Value + "=" + str(Roll + int(Fencing_Value)))
                    else:
                        await message.channel.send("Treffer " + "**" + str(Roll) + "**+" + Fencing_Value + "=" + str(Roll + int(Fencing_Value)))
                        await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Schaden"] + "W6+" + str(int(Current_Attack_Set[i]["Modifikator"])-int(Current_Property_Set[9]["Wert"])) + ")")

#Command listing currently available weapons of the players.
    if message.content == "!Waffen" or message.content == "!waffen":
        await message.channel.send("Waffen, die momentan zur Verfügung stehen:")
        for i in range(len(Current_Attack_Set)):
            await message.channel.send(umlaute(Current_Attack_Set[i]["Name"]) + " (" + Current_Attack_Set[i]["Schaden"] + "W6+" + Current_Attack_Set[i]["Modifikator"] + ")")

#Command listing currently available spells of the players.
    if message.content == "!zauber" or message.content == "!Zauber":
        if len(Current_Spell_List) == 0:
            await channel.message.send("Du erinnerst dich plötzlich, dass du keine Ahnung von Magie hast.")
        else:
            output = "Die Zauber die dir zur Verfügung stehen sind:\n```"
            for i in range(len(Current_Spell_List)):
                output = output + umlaute(Current_Spell_List[i]["Name"]) + "\n"
            await message.channel.send(output + "```Für weitere Information benutze **!info + Zaubername**")

#Command giving info on individual items like spells and items.
    if message.content.startswith("!info") or message.content.startswith("!Info"):
    	item = message.content[6:].lower()
    	if item == "zaubername":
    		await message.channel.send("https://i.imgflip.com/3kk1hj.jpg")
    	else:
    		for i in range(len(Spell_List)):
    			if umlaute(Spell_List[i]["Name"].lower()) == item:
    				await message.channel.send(umlaute("```" + item.capitalize() + " (" + Spell_List[i]["Methode"] + " aus der Schule der " + Spell_List[i]["Schule"] + ")\n\n" + "AP-Verbrauch: " + Spell_List[i]["AP-Verbrauch"] + "\nZauberdauer: " + Spell_List[i]["Zauberdauer"] + "\nReichweite: " + Spell_List[i]["Reichweite"] + "\nWirkungsziel: " + Spell_List[i]["Wirkungsziel"] + "\nWirkungsbereich: " + Spell_List[i]["Wirkungsbereich"] + "\nWirkungsdauer: " + Spell_List[i]["Wirkungsdauer"] + "\nUrsprung: " + Spell_List[i]["Ursprung"] + "\n\n" + Spell_List[i]["Effekt"] + "```"))

#Command rolling a random dice.
    if message.content.startswith("!w ") or message.content.startswith("!W "):
        Number = message.content[3:]
        try:
            await message.channel.send("**" + str(random.randint(1, int(Number))) + "**")
        except:
            await message.channel.send("https://i.imgflip.com/3kk1hj.jpg")
    elif message.content.startswith("!w") or message.content.startswith("!W"):
        Number = message.content[2:]
        try:
            await message.channel.send("**" + str(random.randint(1, int(Number))) + "**")
        except:
            await message.channel.send("https://i.imgflip.com/3kk1hj.jpg")

client.run('TOKEN')
