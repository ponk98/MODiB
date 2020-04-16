import os
import discord, random, json

#Innitialising game data.
Json = open('Game Data/Crits_Fails_Attack.json', 'r')
Crits = json.load(Json)
Crit_Fails_Attack = list(Crits)
Json.close
Json = open('Game Data/Crits_Success_Attack.json', 'r')
Crits = json.load(Json)
Crit_Success_Attack = list(Crits)
Json.close
Json = open('Game Data/Crits_Fails_Defense.json', 'r')
Crits = json.load(Json)
Crit_Fails_Defense = list(Crits)
Json.close
Json = open('Game Data/Crits_Success_Defense.json', 'r')
Crits = json.load(Json)
Crit_Success_Defense = list(Crits)
Json.close
Json = open('Game Data/Crits_Fails_Spells.json', 'r')
Crits = json.load(Json)
Crit_Fails_Spells = list(Crits)
Json.close
Json = open('Game Data/Spell_List.json', 'r')
Spells = json.load(Json)
Spell_List = list(Spells)
Json.close

#Innitialising properties of all characters.
Json = open('Sample Character Data/Properties/Properties_Taravan.json', 'r')
Properties = json.load(Json)
Property_List_Taravan = list(Properties)
Json.close
Json = open('Sample Character Data/Properties/Properties_Cloi.json', 'r')
Properties = json.load(Json)
Property_List_Cloi = list(Properties)
Json.close
Json = open('Sample Character Data/Properties/Properties_Cordovan.json', 'r')
Properties = json.load(Json)
Property_List_Cordovan = list(Properties)
Json.close
Json = open('Sample Character Data/Properties/Properties_Leonidas.json', 'r')
Properties = json.load(Json)
Property_List_Leonidas = list(Properties)
Json.close

#Innitialising abilities of all characters.
Json = open('Sample Character Data/Abilities/Abilities_Cloi.json', 'r')
Abilities = json.load(Json)
Ability_List_Cloi = list(Abilities)
Json.close
Json = open('Sample Character Data/Abilities/Abilities_Cordovan.json', 'r')
Abilities = json.load(Json)
Ability_List_Cordovan = list(Abilities)
Json.close
Json = open('Sample Character Data/Abilities/Abilities_Leonidas.json', 'r')
Abilities = json.load(Json)
Ability_List_Leonidas = list(Abilities)
Json.close
Json = open('Sample Character Data/Abilities/Abilities_Taravan.json', 'r')
Abilities = json.load(Json)
Ability_List_Taravan = list(Abilities)
Json.close

#Innitialising spells of all caster characters.
Json = open('Sample Character Data/Spells/Spells_Cloi.json', 'r')
Spells = json.load(Json)
Spell_List_Cloi = list(Spells)
Json.close
Json = open('Sample Character Data/Spells/Spells_Cordovan.json', 'r')
Spells = json.load(Json)
Spell_List_Cordovan = list(Spells)
Json.close
Json = open('Sample Character Data/Spells/Spells_Taravan.json', 'r')
Spells = json.load(Json)
Spell_List_Taravan = list(Spells)
Json.close

#Innitialising weapons of all characters.
Json = open('Sample Character Data/Weapons/Weapons_Cloi.json', 'r')
Weapons = json.load(Json)
Weapon_List_Cloi = list(Weapons)
Json.close
Json = open('Sample Character Data/Weapons/Weapons_Cordovan.json', 'r')
Weapons = json.load(Json)
Weapon_List_Cordovan = list(Weapons)
Json.close
Json = open('Sample Character Data/Weapons/Weapons_Leonidas.json', 'r')
Weapons = json.load(Json)
Weapon_List_Leonidas = list(Weapons)
Json.close
Json = open('Sample Character Data/Weapons/Weapons_Taravan.json', 'r')
Weapons = json.load(Json)
Weapon_List_Taravan = list(Weapons)
Json.close

#Function that fixes the Umlaute problem
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

#Function that calculates the damage bonus of the currently loaded character
def damage_bonus(Character):
    return int((int(float(Character[4]["Wert"])/20))+int((float(Character[0]["Wert"])/30))-3)

def attack_bonus(Character, Weapons):
    bonus = -2
    if int(Character[0]["Wert"]) > 5:
        bonus = -1
    if int(Character[0]["Wert"]) > 20:
        bonus = 0
    if int(Character[0]["Wert"]) > 80:
        bonus = 1
    if int(Character[0]["Wert"]) > 95:
        bonus = 2
    if Weapons["Spezialisierung"] == "y":
        bonus += 2
    return bonus

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

#Assigns correct weapons, abilities and stats aswell as dm status to the current user based on Discord name of latest message author. Updated on every message.
    if str(message.author) == "Echtgeilman92#2052":
        Current_Attack_Set = Weapon_List_Cloi
        Current_Ability_Set = Ability_List_Cloi
        Current_Property_Set = Property_List_Cloi
        Current_Spell_List = Spell_List_Cloi
        DM_Status = False
    if str(message.author) == "Aelron#6030":
        Current_Attack_Set = Weapon_List_Cordovan
        Current_Ability_Set = Ability_List_Cordovan
        Current_Property_Set = Property_List_Cordovan
        Current_Spell_List = Spell_List_Cordovan
        DM_Status = False
    if str(message.author) == "JohannesDberg#9702":
        Current_Attack_Set = Weapon_List_Leonidas
        Current_Ability_Set = Ability_List_Leonidas
        Current_Property_Set = Property_List_Leonidas
        Current_Spell_List = []
        DM_Status = False
    if str(message.author) == "Friedrich#6066":
        Current_Attack_Set = Weapon_List_Taravan
        Current_Ability_Set = Ability_List_Taravan
        Current_Property_Set = Property_List_Taravan
        Current_Spell_List = Spell_List_Taravan
        DM_Status = False
    if str(message.author) == 'Ponk#0213':
        DM_Status = True

###----------------------------------------------------
#Commands for players to engage with gameplay mechanics
###----------------------------------------------------

#Command handling standard attack commands.
    if message.content.startswith('!Angriff') or message.content.startswith('!angriff'):
        Weapon = message.content[9:].lower()
        for i in range(len(Current_Attack_Set)):
            if umlaute(Weapon) == umlaute(Current_Attack_Set[i]["Name"].lower()):
                Roll = random.randint(1,20)
                Grundschaden = 0
                for j in range(int(Current_Attack_Set[i]["Grundschaden"])):
                    Grundschaden += random.randint(1,6)
                Schaden = Grundschaden + damage_bonus(Current_Property_Set) + int(Current_Attack_Set[i]["Magischer Schadensbonus"])
                if Roll == 20:
                    Effekt = random.randint(1,100)
                    await message.channel.send("**Kritischer Erfolg!** Nebeneffekt: " + str(Effekt))
                    await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Grundschaden"] + "W6+" + str(damage_bonus(Current_Property_Set)+int(Current_Attack_Set[i]["Magischer Schadensbonus"])) + ")")
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
                    if Roll + int(Current_Attack_Set[i]["Fertigkeitswert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]) + attack_bonus(Current_Property_Set, Current_Attack_Set[i]) < 20:
                        await message.channel.send("Kein Treffer " + "**" + str(Roll) + "**+" + str(int(Current_Attack_Set[i]["Fertigkeitswert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]) + attack_bonus(Current_Property_Set, Current_Attack_Set[i])) + "=" + str(Roll + int(Current_Attack_Set[i]["Fertigkeitswert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]) + attack_bonus(Current_Property_Set, Current_Attack_Set[i])))
                    else:
                        await message.channel.send("Treffer " + "**" + str(Roll) + "**+" + str(int(Current_Attack_Set[i]["Fertigkeitswert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]) + attack_bonus(Current_Property_Set, Current_Attack_Set[i])) + "=" + str(Roll + int(Current_Attack_Set[i]["Fertigkeitswert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]) + attack_bonus(Current_Property_Set, Current_Attack_Set[i])))
                        await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Grundschaden"] + "W6+" + str(damage_bonus(Current_Property_Set)+int(Current_Attack_Set[i]["Magischer Schadensbonus"])) + ")")

#Command handling fencing attack commands.
    elif message.content.startswith('!Fechtangriff') or message.content.startswith('!fechtangriff'):
        Weapon = message.content[14:].lower()
        for i in range(len(Current_Attack_Set)):
            if umlaute(Weapon) == umlaute(Current_Attack_Set[i]["Name"].lower()):
                Fencing_Value = str(int(Current_Ability_Set[15]["Wert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]))
                Roll = random.randint(1,20)
                Grundschaden = 0
                for j in range(int(Current_Attack_Set[i]["Grundschaden"])):
                    Grundschaden += random.randint(1,6)
                Schaden = Grundschaden + int(Current_Attack_Set[i]["Magischer Schadensbonus"])
                if Roll == 20:
                    Effekt = random.randint(1,100)
                    await message.channel.send("**Kritischer Erfolg!** Nebeneffekt: " + str(Effekt))
                    await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Grundschaden"] + "W6+" + str(int(Current_Attack_Set[i]["Magischer Schadensbonus"])) + ")")
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
                        await message.channel.send("Schaden: **" + str(Schaden) + "**" + " (" + Current_Attack_Set[i]["Grundschaden"] + "W6+" + Current_Attack_Set[i]["Magischer Schadensbonus"] + ")")

#Command handling fall damage.
    elif message.content.startswith('!Fallschaden') or message.content.startswith('!fallschaden'):
        try:
            height = message.content[13:]
            if int(height) > 100:
                await message.channel.send("Tod")
            elif int(height) < 2:
                await message.channel.send("Kein Fallschaden aus dieser Höhe möglich.")
            elif int(height) == 2:
                if random.randint(1,100) >= int(Current_Property_Set[1]['Wert']):
                    await message.channel.send("Du fällst und nimmst **" + str(random.randint(1,6)) + "** (1W6)" + " AP Schaden!")
                else:
                    await message.channel.send("Du fällst und nimmst **" + str(random.randint(1,6)) + "** (1W6)" + " LP und AP Schaden!")
            else:
                if (int(height) % 2) == 1:
                    damage = 0
                    for i in range(int((int(height) - 1) / 2)):
                        damage += random.randint(1, 6)
                    await message.channel.send("Du fällst und nimmst **" + str(damage + 2) + "** (" + str(int((int(height) - 1) / 2)) + "W6+2)" + " LP und AP Schaden")
                else:
                    damage = 0
                    for i in range(int(int(height) / 2)):
                        damage += random.randint(1, 6)
                    await message.channel.send("Du fällst und nimmst **" + str(damage) + "** (" + str(int((int(height) - 1) / 2)) + "W6)" + " LP und AP Schaden")
        except:
            await message.channel.send("Ungültige Fallhöhe")

#Command handling skill checks.
    elif message.content.startswith('!Test') or message.content.startswith('!test'):
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
        elif Ability == 'zaubern' and Roll == 1 or Ability == 'zaubern' and Roll == 20:
            if Roll == 1:
                Effekt = random.randint(1,100)
                await message.channel.send("**Kritischer Misserfolg!** Nebeneffekt: " + str(Effekt))
                for i in range(len(Crit_Fails_Spells)):
                    if int(Crit_Fails_Spells[i]["Wert"]) <= Effekt:
                        Effekt_Ausgabe = Crit_Fails_Spells[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            if Roll == 20:
                await message.channel.send("**Kritischer Erfolg!**")
        else:
            for i in range(len(Current_Ability_Set)):
                if Ability == umlaute(Current_Ability_Set[i]["Ability"].lower()):
                    if Roll == 20:
                        await message.channel.send("Kritischer Erfolg: " + "**" + str(Roll) + "**" + "+" + Current_Ability_Set[i]["Wert"] + "=" + str(Roll+int(Current_Ability_Set[i]["Wert"])))
                    elif Roll == 1:
                        await message.channel.send("Kritischer Misserfolg: " + "**" + str(Roll) + "**" + "+" + Current_Ability_Set[i]["Wert"] + "=" + str(Roll+int(Current_Ability_Set[i]["Wert"])))
                    else:
                        await message.channel.send("**" + str(Roll) + "**" + "+" + Current_Ability_Set[i]["Wert"] + "=" + str(Roll+int(Current_Ability_Set[i]["Wert"])))

#Command listing currently available weapons of the players.
    elif message.content == "!Waffen" or message.content == "!waffen":
        output = "Waffen, die momentan zur Verfügung stehen:\n```"
        for i in range(len(Current_Attack_Set)):
            output = output + umlaute(Current_Attack_Set[i]["Name"]) + " (" + Current_Attack_Set[i]["Grundschaden"] + "W6+" + str(damage_bonus(Current_Property_Set)+int(Current_Attack_Set[i]["Magischer Schadensbonus"])) + " Schaden) mit Angriff von +" + str(int(Current_Attack_Set[i]["Fertigkeitswert"]) + int(Current_Attack_Set[i]["Magischer Angriffsbonus"]) + attack_bonus(Current_Property_Set, Current_Attack_Set[i])) + "\n"
        await message.channel.send(output + "```")

#Command listing currently available spells of the players.
    elif message.content == "!zauber" or message.content == "!Zauber":
        if len(Current_Spell_List) == 0:
            await channel.message.send("Du erinnerst dich plötzlich, dass du keine Ahnung von Magie hast.")
        else:
            output = "Die Zauber die dir zur Verfügung stehen sind:\n```"
            for i in range(len(Current_Spell_List)):
                output = output + umlaute(Current_Spell_List[i]["Name"]) + "\n"
            await message.channel.send(output + "```Für weitere Information benutze **!info + Zaubername**")

#Command giving info on individual items like spells and items.
    elif message.content.startswith("!info") or message.content.startswith("!Info"):
        item = message.content[6:].lower()
        if item == "zaubername":
            await message.channel.send("https://i.imgflip.com/3kk1hj.jpg")
        else:
            for i in range(len(Spell_List)):
                if umlaute(Spell_List[i]["Name"].lower()) == item:
                    await message.channel.send(umlaute("```" + item.capitalize() + " (" + Spell_List[i]["Methode"] + " aus der Schule der " + Spell_List[i]["Schule"] + ")\n\n" + "AP-Verbrauch: " + Spell_List[i]["AP-Verbrauch"] + "\nZauberdauer: " + Spell_List[i]["Zauberdauer"] + "\nReichweite: " + Spell_List[i]["Reichweite"] + "\nWirkungsziel: " + Spell_List[i]["Wirkungsziel"] + "\nWirkungsbereich: " + Spell_List[i]["Wirkungsbereich"] + "\nWirkungsdauer: " + Spell_List[i]["Wirkungsdauer"] + "\nUrsprung: " + Spell_List[i]["Ursprung"] + "\n\n" + Spell_List[i]["Effekt"] + "```"))
                    break

#Command rolling a random dice.
    elif message.content.startswith("!w ") or message.content.startswith("!W "):
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

###----------------------------------------------------
#Commands for the DM to observe and controll gameplay
###----------------------------------------------------

#Command for requesting specific crit effects without having to do an according roll.
    elif message.content.startswith('!crit') and DM_Status:
        try:
            Request = message.content[6:]
            if Request.startswith('fail attack'):
                for i in range(len(Crit_Fails_Attack)):
                    if int(Crit_Fails_Attack[i]["Wert"]) <= int(Request[12:]):
                        Effekt_Ausgabe = Crit_Fails_Attack[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('success attack'):
                for i in range(len(Crit_Success_Attack)):
                    if int(Crit_Success_Attack[i]["Wert"]) <= int(Request[15:]):
                        Effekt_Ausgabe = Crit_Success_Attack[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('fail defense'):
                for i in range(len(Crit_Fails_Defense)):
                    if int(Crit_Fails_Defense[i]["Wert"]) <= int(Request[13:]):
                        Effekt_Ausgabe = Crit_Fails_Defense[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('success defense'):
                for i in range(len(Crit_Success_Defense)):
                    if int(Crit_Success_Defense[i]["Wert"]) <= int(Request[16:]):
                        Effekt_Ausgabe = Crit_Success_Defense[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('fail spells'):
                for i in range(len(Crit_Fails_Spells)):
                    if int(Crit_Fails_Spells[i]["Wert"]) <= int(Request[12:]):
                        Effekt_Ausgabe = Crit_Fails_Spells[i]["Effekt"]
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
        except:
            await message.channel.send('Ungültige Anfrage')

#Command handling heavy normal damage dealt to players.
    elif message.content.startswith('!s. schaden') and DM_Status:
        Target_Damage = message.content[12:].lower()
        if Target_Damage.startswith('cloi'):
            Schaden = int(Target_Damage[5:]) - int(Property_List_Cloi[12]['Wert'])
            if Schaden <= 0:
                Schaden = 0
            Property_List_Cloi[14]['Wert'] = str(int(Property_List_Cloi[14]['Wert']) - Schaden)
            if int(Property_List_Cloi[14]['Wert']) * 2 < int(Property_List_Cloi[13]['Wert']):
            	Property_List_Cloi[16]['Wert'] = str(int(int(Property_List_Cloi[15]['Wert']) / 2))
            	Property_List_Cloi[18]['Wert'] = str(int(int(Property_List_Cloi[17]['Wert']) / 2))
            else:
            	Property_List_Cloi[16]['Wert'] = str(int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]))
            await message.channel.send('Cloi wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[5:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Cloi[14]['Wert'] + '** LP und **' + Property_List_Cloi[16]['Wert'] + '** AP.')
        elif Target_Damage.startswith('cordovan'):
            Schaden = int(Target_Damage[5:]) - int(Property_List_Cordovan[12]['Wert'])
            if Schaden <= 0:
                Schaden = 0
            Property_List_Cordovan[14]['Wert'] = str(int(Property_List_Cordovan[14]['Wert']) - Schaden)
            if int(Property_List_Cordovan[14]['Wert']) * 2 < int(Property_List_Cordovan[13]['Wert']):
            	Property_List_Cordovan[16]['Wert'] = str(int(int(Property_List_Cordovan[15]['Wert']) / 2))
            	Property_List_Cordovan[18]['Wert'] = str(int(int(Property_List_Cordovan[17]['Wert']) / 2))
            else:
            	Property_List_Cordovan[16]['Wert'] = str(int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[5:]))
            await message.channel.send('Cordovan wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[5:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Cordovan[14]['Wert'] + '** LP und **' + Property_List_Cordovan[16]['Wert'] + '** AP.')
        elif Target_Damage.startswith('leonidas'):
            Schaden = int(Target_Damage[5:]) - int(Property_List_Leonidas[12]['Wert'])
            if Schaden <= 0:
                Schaden = 0
            Property_List_Leonidas[14]['Wert'] = str(int(Property_List_Leonidas[14]['Wert']) - Schaden)
            if int(Property_List_Leonidas[14]['Wert']) * 2 < int(Property_List_Leonidas[13]['Wert']):
            	Property_List_Leonidas[16]['Wert'] = str(int(int(Property_List_Leonidas[15]['Wert']) / 2))
            	Property_List_Leonidas[18]['Wert'] = str(int(int(Property_List_Leonidas[17]['Wert']) / 2))
            else:
            	Property_List_Leonidas[16]['Wert'] = str(int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[5:]))
            await message.channel.send('Leonidas wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[5:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Leonidas[14]['Wert'] + '** LP und **' + Property_List_Leonidas[16]['Wert'] + '** AP.')
        elif Target_Damage.startswith('taravan'):
            Schaden = int(Target_Damage[5:]) - int(Property_List_Taravan[12]['Wert'])
            if Schaden <= 0:
                Schaden = 0
            Property_List_Cloi[14]['Wert'] = str(int(Property_List_Taravan[14]['Wert']) - Schaden)
            if int(Property_List_Taravan[14]['Wert']) * 2 < int(Property_List_Taravan[13]['Wert']):
            	Property_List_Taravan[16]['Wert'] = str(int(int(Property_List_Taravan[15]['Wert']) / 2))
            	Property_List_Taravan[18]['Wert'] = str(int(int(Property_List_Taravan[17]['Wert']) / 2))
            else:
            	Property_List_Taravan[16]['Wert'] = str(int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[5:]))
            await message.channel.send('Taravan wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[5:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Taravan[14]['Wert'] + '** LP und **' + Property_List_Taravan[16]['Wert'] + '** AP.')

client.run('TOKEN')