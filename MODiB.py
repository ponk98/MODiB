import os
import youtube_dl
import discord, random, json

#Function that calculates the damage bonus of the currently loaded character
def damage_bonus(Character):
    return int((int(float(Character[4]['Wert'])/20))+int((float(Character[0]['Wert'])/30))-3)

#Fnction that calculates the attack bonus of the currently loaded character
def attack_bonus(Character, KiV, Weapons):
    bonus = -2
    if int(Character[0]['Wert']) > 5:
        bonus = -1
    if int(Character[0]['Wert']) > 20:
        bonus = 0
    if int(Character[0]['Wert']) > 80:
        bonus = 1
        if int(Character[12]['Wert']) >= 5 and int(KiV) < 5:
            bonus = 0
    if int(Character[0]['Wert']) > 95:
        bonus = 2
        if int(Character[12]['Wert']) == 5 and int(KiV) < 5:
            bonus = 1
        if int(Character[12]['Wert']) == 6 and int(KiV) < 5:
            bonus = 0
    if Weapons['Spezialisierung'] == 'y':
        bonus += 2
    return bonus

#Function that computes all the property changes that come with armor changes
def armor_changes(Character, Armor, Abilities):
    Changes = [Character[12]['Wert'], Character[9]['Wert'], Character[18]['Wert'], 'Ungültiger Rüstungswert']
    if Armor <= 2:
        Changes[0] = str(Armor)
        Changes[1] = Character[1]['Wert']
        Changes[2] = Character[17]['Wert']
        Changes[3] = 'Rüstung erfolgreich angepasst.'
    elif Armor == 3:
        if int(Character[4]['Wert']) >= 31:
            Changes[0] = str(Armor)
            Changes[1] = Character[1]['Wert']
            if int(Abilities[24]['Wert']) < 5:
                Neue_B = int(Character[17]['Wert']) - 4
                if Neue_B < 0:
                    Neue_B = 0
                Changes[2] = str(Neue_B)
            else:
                Changes[2] = Character[17]['Wert']
            Changes[3] = 'Rüstung erfolgreich angepasst.'
        else:
            Changes[3] = 'Du bist nicht stark genug um Kettenrüstung zu tragen.'
    elif Armor == 4:
        if int(Character[4]['Wert']) >= 61:
            Changes[0] = str(Armor)
            if int(Abilities[24]['Wert']) < 5:
                Neue_GW = int(Character[1]['Wert']) - 25
                if Neue_GW < 0:
                    Neue_GW = 0
                Changes[1] = Neue_GW
                Neue_B = int(Character[17]['Wert']) - 8
                if Neue_B < 0:
                    Neue_B = 0
                Changes[2] = str(Neue_B)
            else:
                Changes[1] = Character[1]['Wert']
                Changes[2] = Character[17]['Wert']
            Changes[3] = 'Rüstung erfolgreich angepasst.'
        else:
            Changes[3] = 'Du bist nicht stark genug um Plattenrüstung zu tragen.'
    elif Armor == 5:
        if int(Character[4]['Wert']) >= 61:
            Changes[0] = str(Armor)
            if int(Abilities[24]['Wert']) < 5:
                Neue_GW = int(Character[1]['Wert']) - 40
                if Neue_GW < 0:
                    Neue_GW = 0
                Changes[1] = Neue_GW
                Neue_B = int(Character[17]['Wert']) - 12
                if Neue_B < 0:
                    Neue_B = 0
                Changes[2] = str(Neue_B)
            else:
                Changes[1] = Character[1]['Wert']
                Changes[2] = Character[17]['Wert']
            Changes[3] = 'Rüstung erfolgreich angepasst.'
        else:
            Changes[3] = 'Du bist nicht stark genug um Vollrüstung zu tragen.'
    elif Armor == 6:
        if int(Character[4]['Wert']) >= 81:
            Changes[0] = str(Armor)
            if int(Abilities[24]['Wert']) < 5:
                Neue_GW = int(Character[1]['Wert']) - 50
                if Neue_GW < 0:
                    Neue_GW = 0
                Changes[1] = Neue_GW
                Neue_B = int(Character[17]['Wert']) - 16
                if Neue_B < 0:
                    Neue_B = 0
                Changes[2] = str(Neue_B)
            else:
                Changes[1] = Character[1]['Wert']
                Changes[2] = Character[17]['Wert']
            Changes[3] = 'Rüstung erfolgreich angepasst.'
        else:
            Changes[3] = 'Du bist nicht stark genug um Ritterrüstung zu tragen.'
    return Changes

###----------------------------------------------------
#Functions that handle gamedata and frontend things
###----------------------------------------------------

#Function that loads character unspecific gamedata
def load_game_data():
    Json = open('Game Data/Crits_Fails_Attack.json', 'r')
    Crits = json.load(Json)
    global Crit_Fails_Attack
    Crit_Fails_Attack = list(Crits)
    Json.close
    Json = open('Game Data/Crits_Success_Attack.json', 'r')
    Crits = json.load(Json)
    global Crit_Success_Attack
    Crit_Success_Attack = list(Crits)
    Json.close
    Json = open('Game Data/Crits_Fails_Defense.json', 'r')
    Crits = json.load(Json)
    global Crit_Fails_Defense
    Crit_Fails_Defense = list(Crits)
    Json.close
    Json = open('Game Data/Crits_Success_Defense.json', 'r')
    Crits = json.load(Json)
    global Crit_Success_Defense
    Crit_Success_Defense = list(Crits)
    Json.close
    Json = open('Game Data/Crits_Fails_Spells.json', 'r')
    Crits = json.load(Json)
    global Crit_Fails_Spells
    Crit_Fails_Spells = list(Crits)
    Json.close
    Json = open('Game Data/Crits_Injuries.json', 'r')
    Injuries = json.load(Json)
    global Injury_List
    Injury_List = list(Injuries)
    Json.close
    Json = open('Game Data/Falldamage.json', 'r')
    Fall = json.load(Json)
    global Fall_Damage_Effects
    Fall_Damage_Effects = list(Fall)
    Json.close
    Json = open('Game Data/Spell_List.json', 'r')
    Spells = json.load(Json)
    global Spell_List
    Spell_List = list(Spells)
    Json.close

#Function that loads character specific gamedata
def load_character_data():

    #Innitialising properties of all characters.
    Json = open('Sample Character Data/Properties/Properties_Taravan.json', 'r')
    Properties = json.load(Json)
    global Property_List_Taravan
    Property_List_Taravan = list(Properties)
    Json.close
    Json = open('Sample Character Data/Properties/Properties_Cloi.json', 'r')
    Properties = json.load(Json)
    global Property_List_Cloi
    Property_List_Cloi = list(Properties)
    Json.close
    Json = open('Sample Character Data/Properties/Properties_Cordovan.json', 'r')
    Properties = json.load(Json)
    global Property_List_Cordovan
    Property_List_Cordovan = list(Properties)
    Json.close
    Json = open('Sample Character Data/Properties/Properties_Leonidas.json', 'r')
    Properties = json.load(Json)
    global Property_List_Leonidas
    Property_List_Leonidas = list(Properties)
    Json.close

    #Innitialising abilities of all characters.
    Json = open('Sample Character Data/Abilities/Abilities_Cloi.json', 'r')
    Abilities = json.load(Json)
    global Ability_List_Cloi
    Ability_List_Cloi = list(Abilities)
    Json.close
    Json = open('Sample Character Data/Abilities/Abilities_Cordovan.json', 'r')
    Abilities = json.load(Json)
    global Ability_List_Cordovan
    Ability_List_Cordovan = list(Abilities)
    Json.close
    Json = open('Sample Character Data/Abilities/Abilities_Leonidas.json', 'r')
    Abilities = json.load(Json)
    global Ability_List_Leonidas
    Ability_List_Leonidas = list(Abilities)
    Json.close
    Json = open('Sample Character Data/Abilities/Abilities_Taravan.json', 'r')
    Abilities = json.load(Json)
    global Ability_List_Taravan
    Ability_List_Taravan = list(Abilities)
    Json.close

    #Innitialising spells of all caster characters.
    Json = open('Sample Character Data/Spells/Spells_Cloi.json', 'r')
    Spells = json.load(Json)
    global Spell_List_Cloi
    Spell_List_Cloi = list(Spells)
    Json.close
    Json = open('Sample Character Data/Spells/Spells_Cordovan.json', 'r')
    Spells = json.load(Json)
    global Spell_List_Cordovan
    Spell_List_Cordovan = list(Spells)
    Json.close
    Json = open('Sample Character Data/Spells/Spells_Taravan.json', 'r')
    Spells = json.load(Json)
    global Spell_List_Taravan
    Spell_List_Taravan = list(Spells)
    Json.close

    #Innitialising weapons of all characters.
    Json = open('Sample Character Data/Weapons/Weapons_Cloi.json', 'r')
    Weapons = json.load(Json)
    global Weapon_List_Cloi
    Weapon_List_Cloi = list(Weapons)
    Json.close
    Json = open('Sample Character Data/Weapons/Weapons_Cordovan.json', 'r')
    Weapons = json.load(Json)
    global Weapon_List_Cordovan
    Weapon_List_Cordovan = list(Weapons)
    Json.close
    Json = open('Sample Character Data/Weapons/Weapons_Leonidas.json', 'r')
    Weapons = json.load(Json)
    global Weapon_List_Leonidas
    Weapon_List_Leonidas = list(Weapons)
    Json.close
    Json = open('Sample Character Data/Weapons/Weapons_Taravan.json', 'r')
    Weapons = json.load(Json)
    global Weapon_List_Taravan
    Weapon_List_Taravan = list(Weapons)
    Json.close

#Function that saves character specific gamedata
def save_data():
    Data = open('Sample Character Data/Properties/Properties_Cloi.json', 'r+')
    Data.write(str(Property_List_Cloi).replace('}, ', '},\n').replace(']', '\n]').replace('[', '[\n').replace("'", '"'))
    Data.close
    Data = open('Sample Character Data/Properties/Properties_Cordovan.json', 'r+')
    Data.write(str(Property_List_Cordovan).replace('}, ', '},\n').replace(']', '\n]').replace('[', '[\n').replace("'", '"'))
    Data.close
    Data = open('Sample Character Data/Properties/Properties_Leonidas.json', 'r+')
    Data.write(str(Property_List_Leonidas).replace('}, ', '},\n').replace(']', '\n]').replace('[', '[\n').replace("'", '"'))
    Data.close
    Data = open('Sample Character Data/Properties/Properties_Taravan.json', 'r+')
    Data.write(str(Property_List_Taravan).replace('}, ', '},\n').replace(']', '\n]').replace('[', '[\n').replace("'", '"'))
    Data.close

#Function that fixes the Umlaute problem
def umlaute(string):
    string = string.replace('ã¤', 'ä')
    string = string.replace('Ã¤', 'ä')
    string = string.replace('Ãœ', 'Ü')
    string = string.replace('ã¼', 'ü')
    string = string.replace('Ã¼', 'ü')
    string = string.replace('ã¶', 'ö')
    string = string.replace('Ã¶', 'ö')
    string = string.replace('ÃŸ', 'ß')
    string = string.replace('â€“', '–')
    return string

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Loading data...')
    load_game_data()
    load_character_data()
    print('Loading complete.')

@client.event
async def on_message(message):

#Assigns correct weapons, abilities and stats aswell as dm status to the current user based on Discord name of latest message author. Updated on message.
    if str(message.author) == 'Echtgeilman92#2052':
        Current_Attack_Set = Weapon_List_Cloi
        Current_Ability_Set = Ability_List_Cloi
        Current_Property_Set = Property_List_Cloi
        Current_Spell_List = Spell_List_Cloi
        DM_Status = False
    if str(message.author) == 'Aelron#6030' or str(message.author) == 'Ponk#0213':
        Current_Attack_Set = Weapon_List_Cordovan
        Current_Ability_Set = Ability_List_Cordovan
        Current_Property_Set = Property_List_Cordovan
        Current_Spell_List = Spell_List_Cordovan
        DM_Status = False
    if str(message.author) == 'JohannesDberg#9702':
        Current_Attack_Set = Weapon_List_Leonidas
        Current_Ability_Set = Ability_List_Leonidas
        Current_Property_Set = Property_List_Leonidas
        Current_Spell_List = []
        DM_Status = False
    if str(message.author) == 'Friedrich#6066':
        Current_Attack_Set = Weapon_List_Taravan
        Current_Ability_Set = Ability_List_Taravan
        Current_Property_Set = Property_List_Taravan
        Current_Spell_List = Spell_List_Taravan
        DM_Status = False
    if str(message.author) == 'Ponk#0213':
        DM_Status = True

###----------------------------------------------------
#Commands for players and DM to engage with gameplay mechanics
###----------------------------------------------------

#Command handling standard attack commands.
    if message.content.lower().startswith('!angriff'):
        Weapon = message.content[9:].lower()
        for i in range(len(Current_Attack_Set)):
            if umlaute(Weapon) == umlaute(Current_Attack_Set[i]['Name'].lower()):
                Roll = random.randint(1,20)
                Grundschaden = 0
                for j in range(int(Current_Attack_Set[i]['Grundschaden'])):
                    Grundschaden += random.randint(1,6)
                Schaden = Grundschaden + int(Current_Attack_Set[i]['Modifikator']) + damage_bonus(Current_Property_Set) + int(Current_Attack_Set[i]['Magischer Schadensbonus'])
                if Roll == 20:
                    Effekt = random.randint(1,100)
                    await message.channel.send('**Kritischer Erfolg!** Nebeneffekt: ' + str(Effekt))
                    await message.channel.send('Schaden: **' + str(Schaden) + '**' + ' (' + Current_Attack_Set[i]['Grundschaden'] + 'W6+' + str(damage_bonus(Current_Property_Set) + int(Current_Attack_Set[i]['Modifikator']) + int(Current_Attack_Set[i]['Magischer Schadensbonus'])) + ')')
                    for i in range(len(Crit_Success_Attack)):
                        if int(Crit_Success_Attack[i]['Wert']) <= Effekt:
                            Effekt_Ausgabe = Crit_Success_Attack[i]['Effekt']
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                elif Roll == 1:
                    Effekt = random.randint(1,100)
                    await message.channel.send('**Kritischer Misserfolg!** Nebeneffekt: ' + str(Effekt))
                    for i in range(len(Crit_Fails_Attack)):
                        if int(Crit_Fails_Attack[i]['Wert']) <= Effekt:
                            Effekt_Ausgabe = Crit_Fails_Attack[i]['Effekt']
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                else:
                    if Roll + int(Current_Attack_Set[i]['Fertigkeitswert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']) + attack_bonus(Current_Property_Set, Current_Ability_Set[24]['Wert'], Current_Attack_Set[i]) < 20:
                        await message.channel.send('Kein Treffer ' + '**' + str(Roll) + '**+' + str(int(Current_Attack_Set[i]['Fertigkeitswert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']) + attack_bonus(Current_Property_Set, Current_Ability_Set[24]['Wert'], Current_Attack_Set[i])) + '=' + str(Roll + int(Current_Attack_Set[i]['Fertigkeitswert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']) + attack_bonus(Current_Property_Set, Current_Ability_Set[24]['Wert'], Current_Attack_Set[i])))
                    else:
                        await message.channel.send('Treffer ' + '**' + str(Roll) + '**+' + str(int(Current_Attack_Set[i]['Fertigkeitswert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']) + attack_bonus(Current_Property_Set, Current_Ability_Set[24]['Wert'], Current_Attack_Set[i])) + '=' + str(Roll + int(Current_Attack_Set[i]['Fertigkeitswert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']) + attack_bonus(Current_Property_Set, Current_Ability_Set[24]['Wert'], Current_Attack_Set[i])))
                        await message.channel.send('Schaden: **' + str(Schaden) + '**' + ' (' + Current_Attack_Set[i]['Grundschaden'] + 'W6+' + str(damage_bonus(Current_Property_Set) + int(Current_Attack_Set[i]['Modifikator']) + int(Current_Attack_Set[i]['Magischer Schadensbonus'])) + ')')

#Command handling fencing attack commands.
    elif message.content.lower().startswith('!fechtangriff'):
        Weapon = message.content[14:].lower()
        for i in range(len(Current_Attack_Set)):
            if umlaute(Weapon) == umlaute(Current_Attack_Set[i]['Name'].lower()):
                Fencing_Value = str(int(Current_Ability_Set[15]['Wert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']))
                Roll = random.randint(1,20)
                Grundschaden = 0
                for j in range(int(Current_Attack_Set[i]['Grundschaden'])):
                    Grundschaden += random.randint(1,6)
                Schaden = Grundschaden + int(Current_Attack_Set[i]['Magischer Schadensbonus']) + int(Current_Attack_Set[i]['Modifikator'])
                if Roll == 20:
                    Effekt = random.randint(1,100)
                    await message.channel.send('**Kritischer Erfolg!** Nebeneffekt: ' + str(Effekt))
                    await message.channel.send('Schaden: **' + str(Schaden) + '**' + ' (' + Current_Attack_Set[i]['Grundschaden'] + 'W6+' + str(int(Current_Attack_Set[i]['Magischer Schadensbonus']) + int(Current_Attack_Set[i]['Modifikator'])) + ')')
                    for i in range(len(Crit_Success_Attack)):
                        if int(Crit_Success_Attack[i]['Wert']) <= Effekt:
                            Effekt_Ausgabe = Crit_Success_Attack[i]['Effekt']
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                elif Roll == 1:
                    Effekt = random.randint(1,100)
                    await message.channel.send('**Kritischer Misserfolg!** Nebeneffekt: ' + str(Effekt))
                    for i in range(len(Crit_Fails_Attack)):
                        if int(Crit_Fails_Attack[i]['Wert']) <= Effekt:
                            Effekt_Ausgabe = Crit_Fails_Attack[i]['Effekt']
                        else:
                            break
                    await message.channel.send(umlaute(Effekt_Ausgabe))
                else:
                    if Roll + int(Fencing_Value) < 20:
                        await message.channel.send('Kein Treffer ' + '**' + str(Roll) + '**+' + Fencing_Value + '=' + str(Roll + int(Fencing_Value)))
                    else:
                        await message.channel.send('Treffer ' + '**' + str(Roll) + '**+' + Fencing_Value + '=' + str(Roll + int(Fencing_Value)))
                        await message.channel.send('Schaden: **' + str(Schaden) + '**' + ' (' + Current_Attack_Set[i]['Grundschaden'] + 'W6+' + str(int(Current_Attack_Set[i]['Magischer Schadensbonus']) + int(Current_Attack_Set[i]['Modifikator'])) + ')')

#Command handling skill checks.
    elif message.content.lower().startswith('!test'):
        Ability = message.content[6:].lower()
        Roll = random.randint(1,20)
        if Ability == 'abwehr' and Roll == 1 or Ability == 'abwehr' and Roll == 20:
            if Roll == 1:
                Effekt = random.randint(1,100)
                await message.channel.send('**Kritischer Misserfolg!** Nebeneffekt: ' + str(Effekt))
                for i in range(len(Crit_Fails_Defense)):
                    if int(Crit_Fails_Defense[i]['Wert']) <= Effekt:
                        Effekt_Ausgabe = Crit_Fails_Defense[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            if Roll == 20:
                Effekt = random.randint(1,100)
                await message.channel.send('**Kritischer Erfolg!** Nebeneffekt: ' + str(Effekt))
                for i in range(len(Crit_Success_Defense)):
                    if int(Crit_Success_Defense[i]['Wert']) <= Effekt:
                        Effekt_Ausgabe = Crit_Success_Defense[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
        else:
            for i in range(len(Current_Ability_Set)):
                if Ability == umlaute(Current_Ability_Set[i]['Ability'].lower()):
                    if Roll == 20:
                        await message.channel.send('Kritischer Erfolg: ' + '**' + str(Roll) + '**' + '+' + Current_Ability_Set[i]['Wert'] + '=' + str(Roll+int(Current_Ability_Set[i]['Wert'])))
                    elif Roll == 1:
                        await message.channel.send('Kritischer Misserfolg: ' + '**' + str(Roll) + '**' + '+' + Current_Ability_Set[i]['Wert'] + '=' + str(Roll+int(Current_Ability_Set[i]['Wert'])))
                    else:
                        await message.channel.send('**' + str(Roll) + '**' + '+' + Current_Ability_Set[i]['Wert'] + '=' + str(Roll+int(Current_Ability_Set[i]['Wert'])))

#Command handling spell checks.
    elif message.content.lower().startswith('!zaubern'):
        #try:
        spell_amount = message.content[9:].lower()
        amounts = [int(d) for d in spell_amount.split() if d.isdigit()]
        if len(amounts) > 1:
            await message.channel.send('Zu viele Parameter angegeben!')
            AP_Kosten = 0
        elif len(amounts) == 0:
            spell = spell_amount
            spell_known = False
            for i in range(len(Current_Spell_List)):
                if spell == umlaute(Current_Spell_List[i]['Name']).lower():
                    spell_known = True
            if not spell_known:
                await message.channel.send('Der Zauber ist entweder nicht gelernt oder existiert nicht!')
                AP_Kosten = 0
            elif spell_known:
                for i in range(len(Spell_List)):
                    if spell == umlaute(Spell_List[i]['Name']).lower():
                        index = i
                        break
                cost = Spell_List[i]['AP-Verbrauch']
                if "je" in cost:
                    await message.channel.send('Der Zauber hat variable AP Kosten. Der Zauber kostet ' + Spell_List[index]['AP-Verbrauch'] + '. Wiederhole den Befehl und füge die gewünschte Anzahl hinten an.')
                    AP_Kosten = 0
                else:
                    AP_Kosten = int(Spell_List[index]['AP-Verbrauch'])
                    if AP_Kosten > int(Current_Property_Set[16]['Wert']):
                        await message.channel.send('Du hast nicht genügend AP um diesen Zauber zu wirken!')
                        AP_Kosten = 0
                    else:
                        Roll = random.randint(1,20)
                        if Roll == 1:
                            Effekt = random.randint(1,100)
                            output = '**Der Zauber ist ein kritischer Misserfolg!** Nebeneffekt: ' + str(Effekt)
                            for i in range(len(Crit_Fails_Spells)):
                                if int(Crit_Fails_Spells[i]['Wert']) <= Effekt:
                                    Effekt_Ausgabe = umlaute(Crit_Fails_Spells[i]['Effekt'])
                                else:
                                    break
                            if Effekt > 10 and Effekt < 31:
                                x = random.randint(1, 6)
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('1W6', ('**' + str(x) + '** (1W6)'))
                            elif Effekt > 30 and Effekt < 51:
                                AP_Kosten = AP_Kosten*2
                            elif Effekt > 70 and Effekt < 81:
                                x = random.randint(1, 6)
                                y = random.randint(1, 6)
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('1W6 AP', ('**' + str(x) + '** (1W6) AP'))
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('kann 1W6', ('kann **' + str(y) + '** (1W6)'))
                                AP_Kosten += x
                            elif Effekt > 90 and Effekt < 96:
                                x = random.randint(1, 6)
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('1W6', ('**' + str(x) + '** (1W6)'))
                            await message.channel.send(output + '\n' + umlaute(Effekt_Ausgabe))
                        elif Roll == 20:
                            await message.channel.send('**Der Zauber ist ein kritischer Erfolg!**')
                        else:
                            bonus = 0
                            if Spell_List[index]['Schule'] == Current_Property_Set[19]['Wert']:
                                bonus += 2
                            if Roll + bonus + int(Current_Ability_Set[62]['Wert']) >= 20:
                                await message.channel.send('Der Zauber war erfolgreich! ' + str(Roll + bonus + int(Current_Ability_Set[62]['Wert'])) + ' (**' + str(Roll) + '** + ' + str(bonus + int(Current_Ability_Set[62]['Wert'])) + ')')
                            else:
                                await message.channel.send('Der Zauber war nicht erfolgreich! ' + str(Roll + bonus + int(Current_Ability_Set[62]['Wert'])) + ' (**' + str(Roll) + '** + ' + str(bonus + int(Current_Ability_Set[62]['Wert'])) + ')')
        elif len(amounts) == 1:
            spell = spell_amount.replace(str(amounts[0]), '').replace(' ', '')
            spell_known = False
            for i in range(len(Current_Spell_List)):
                if spell == umlaute(Current_Spell_List[i]['Name']).lower().replace(' ', ''):
                    spell_known = True
            if not spell_known:
                await message.channel.send('Der Zauber ist entweder nicht gelernt oder existiert nicht!')
                AP_Kosten = 0
            elif spell_known:
                for i in range(len(Spell_List)):
                    if spell == umlaute(Spell_List[i]['Name']).lower().replace(' ', ''):
                        index = i
                        break
                cost = Spell_List[i]['AP-Verbrauch']
                if "je" not in cost:
                    await message.channel.send('Der Zauber hat keine variablen AP Kosten. Wiederhole den Befehl ohne Anzahl.')
                    AP_Kosten = 0
                else:
                    AP_Kosten = int(Spell_List[index]['AP-Verbrauch'][:1]) * int(amounts[0])
                    if AP_Kosten > int(Current_Property_Set[16]['Wert']):
                        await message.channel.send('Du hast nicht genügend AP um diesen Zauber zu wirken!')
                        AP_Kosten = 0
                    else:
                        Roll = random.randint(1,20)
                        if Roll == 1:
                            Effekt = random.randint(1,100)
                            output = '**Der Zauber ist ein kritischer Misserfolg!** Nebeneffekt: ' + str(Effekt)
                            for i in range(len(Crit_Fails_Spells)):
                                if int(Crit_Fails_Spells[i]['Wert']) <= Effekt:
                                    Effekt_Ausgabe = umlaute(Crit_Fails_Spells[i]['Effekt'])
                                else:
                                    break
                            if Effekt > 10 and Effekt < 31:
                                x = random.randint(1, 6)
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('1W6', ('**' + str(x) + '** (1W6)'))
                            elif Effekt > 30 and Effekt < 51:
                                AP_Kosten = AP_Kosten*2
                            elif Effekt > 70 and Effekt < 81:
                                x = random.randint(1, 6)
                                y = random.randint(1, 6)
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('1W6 AP', ('**' + str(x) + '** (1W6) AP'))
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('kann 1W6', ('kann **' + str(y) + '** (1W6)'))
                                AP_Kosten += x
                            elif Effekt > 90 and Effekt < 96:
                                x = random.randint(1, 6)
                                y = random.randint(1, 6)
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('dadurch 1W6', ('dadurch **' + str(x) + '** (1W6)'))
                                Effekt_Ausgabe = Effekt_Ausgabe.replace('nach 1W6', ('nach **' + str(y) + '** (1W6)'))
                            await message.channel.send(output + '\n' + umlaute(Effekt_Ausgabe))
                        elif Roll == 20:
                            await message.channel.send('**Der Zauber ist ein kritischer Erfolg!**')
                        else:
                            bonus = 0
                            if Spell_List[index]['Schule'] == Current_Property_Set[19]['Wert']:
                                bonus += 2
                            if Roll + bonus + int(Current_Ability_Set[62]['Wert']) >= 20:
                                await message.channel.send('Der Zauber war erfolgreich! ' + str(Roll + bonus + int(Current_Ability_Set[62]['Wert'])) + ' (**' + str(Roll) + '** + ' + str(bonus + int(Current_Ability_Set[62]['Wert'])) + ')')
                            else:
                                await message.channel.send('Der Zauber war nicht erfolgreich! ' + str(Roll + bonus + int(Current_Ability_Set[62]['Wert'])) + ' (**' + str(Roll) + '** + ' + str(bonus + int(Current_Ability_Set[62]['Wert'])) + ')')
        if not AP_Kosten == 0:
            if str(message.author) == 'Echtgeilman92#2052':
                if int(Property_List_Cloi[16]['Wert']) - AP_Kosten < 0:
                    Property_List_Cloi[16]['Wert'] = '0'
                else:
                    Property_List_Cloi[16]['Wert'] = str(int(Property_List_Cloi[16]['Wert']) - AP_Kosten)
                await message.channel.send('Du bist nun bei ' + Property_List_Cloi[16]['Wert'] + ' AP')
            if str(message.author) == 'Aelron#6030' or str(message.author) == 'Ponk#0213':
                if int(Property_List_Cordovan[16]['Wert']) - AP_Kosten < 0:
                    Property_List_Cordovan[16]['Wert'] = '0'
                else:
                    Property_List_Cordovan[16]['Wert'] = str(int(Property_List_Cordovan[16]['Wert']) - AP_Kosten)
                await message.channel.send('Du bist nun bei ' + Property_List_Cordovan[16]['Wert'] + ' AP')
            if str(message.author) == 'JohannesDberg#9702':
                if int(Property_List_Leonidas[16]['Wert']) - AP_Kosten < 0:
                    Property_List_Leonidas[16]['Wert'] = '0'
                else:
                    Property_List_Leonidas[16]['Wert'] = str(int(Property_List_Leonidas[16]['Wert']) - AP_Kosten)
                    await message.channel.send('Du bist nun bei ' + Property_List_Leonidas[16]['Wert'] + ' AP')
            if str(message.author) == 'Friedrich#6066':
                if int(Property_List_Taravan[16]['Wert']) - AP_Kosten < 0:
                    Property_List_Taravan[16]['Wert'] = '0'
                else:
                    Property_List_Taravan[16]['Wert'] = str(int(Property_List_Taravan[16]['Wert']) - AP_Kosten)
                await message.channel.send('Du bist nun bei ' + Property_List_Taravan[16]['Wert'] + ' AP')
            
#Command handling direct damage dealt to any player. (Players can only inflict damage to self, while DM can inflict damage to any player.)
    elif message.content.startswith('!d. schaden'):
        try:
            Target_Damage = message.content[12:].lower()
            if Target_Damage.startswith('cloi') and DM_Status or Target_Damage.startswith('cloi') and str(message.author) == 'Echtgeilman92#2052':
                Schaden = int(Target_Damage[5:])
                Property_List_Cloi[14]['Wert'] = str(int(Property_List_Cloi[14]['Wert']) - Schaden)
                if int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]) < 0:
                    Property_List_Cloi[16]['Wert'] = '0'
                else:
                    Property_List_Cloi[16]['Wert'] = str(int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]))
                if int(Property_List_Cloi[14]['Wert']) * 2 < int(Property_List_Cloi[13]['Wert']) and int(Property_List_Cloi[16]['Wert']) > int(int(Property_List_Cloi[15]['Wert']) / 2):
                    Property_List_Cloi[16]['Wert'] = str(int(int(Property_List_Cloi[15]['Wert']) / 2))
                if int(Property_List_Cloi[14]['Wert']) * 2 < int(Property_List_Cloi[13]['Wert']):
                    Property_List_Cloi[18]['Wert'] = str(int(int(Property_List_Cloi[17]['Wert']) / 2))
                await message.channel.send('Cloi wird direkt getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[5:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Cloi[14]['Wert'] + '** LP und **' + Property_List_Cloi[16]['Wert'] + '** AP.')
            elif Target_Damage.startswith('cordovan') and DM_Status or Target_Damage.startswith('cordovan') and str(message.author) == 'Aelron#6030':
                Schaden = int(Target_Damage[9:])
                Property_List_Cordovan[14]['Wert'] = str(int(Property_List_Cordovan[14]['Wert']) - Schaden)
                if int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[9:]) < 0:
                    Property_List_Cordovan[16]['Wert'] = '0'
                else:
                    Property_List_Cordovan[16]['Wert'] = str(int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[9:]))
                if int(Property_List_Cordovan[14]['Wert']) * 2 < int(Property_List_Cordovan[13]['Wert']) and int(Property_List_Cordovan[16]['Wert']) > int(int(Property_List_Cordovan[15]['Wert']) / 2):
                    Property_List_Cordovan[16]['Wert'] = str(int(int(Property_List_Cordovan[15]['Wert']) / 2))
                if int(Property_List_Cordovan[14]['Wert']) * 2 < int(Property_List_Cordovan[13]['Wert']):
                    Property_List_Cordovan[18]['Wert'] = str(int(int(Property_List_Cordovan[17]['Wert']) / 2))
                await message.channel.send('Cordovan wird direkt getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[9:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Cordovan[14]['Wert'] + '** LP und **' + Property_List_Cordovan[16]['Wert'] + '** AP.')
            elif Target_Damage.startswith('leonidas') and DM_Status or Target_Damage.startswith('leonidas') and str(message.author) == 'JohannesDberg#9702':
                Schaden = int(Target_Damage[9:])
                Property_List_Leonidas[14]['Wert'] = str(int(Property_List_Leonidas[14]['Wert']) - Schaden)
                if int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[9:]) < 0:
                    Property_List_Leonidas[16]['Wert'] = '0'
                else:
                    Property_List_Leonidas[16]['Wert'] = str(int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[9:]))
                if int(Property_List_Leonidas[14]['Wert']) * 2 < int(Property_List_Leonidas[13]['Wert']) and int(Property_List_Leonidas[16]['Wert']) > int(int(Property_List_Leonidas[15]['Wert']) / 2):
                    Property_List_Leonidas[16]['Wert'] = str(int(int(Property_List_Leonidas[15]['Wert']) / 2))
                if int(Property_List_Leonidas[14]['Wert']) * 2 < int(Property_List_Leonidas[13]['Wert']):
                    Property_List_Leonidas[18]['Wert'] = str(int(int(Property_List_Leonidas[17]['Wert']) / 2))
                await message.channel.send('Leonidas wird direkt getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[9:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Leonidas[14]['Wert'] + '** LP und **' + Property_List_Leonidas[16]['Wert'] + '** AP.')
            elif Target_Damage.startswith('taravan') and DM_Status or Target_Damage.startswith('taravan') and str(message.author) == 'Friedrich#6066':
                Schaden = int(Target_Damage[8:]) - int(Property_List_Taravan[12]['Wert'])
                Property_List_Taravan[14]['Wert'] = str(int(Property_List_Taravan[14]['Wert']) - Schaden)
                if int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[8:]) < 0:
                    Property_List_Taravan[16]['Wert'] = '0'
                else:
                    Property_List_Taravan[16]['Wert'] = str(int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[8:]))
                if int(Property_List_Taravan[14]['Wert']) * 2 < int(Property_List_Taravan[13]['Wert']) and int(Property_List_Taravan[16]['Wert']) > int(int(Property_List_Taravan[15]['Wert']) / 2):
                    Property_List_Taravan[16]['Wert'] = str(int(int(Property_List_Taravan[15]['Wert']) / 2))
                if int(Property_List_Taravan[14]['Wert']) * 2 < int(Property_List_Taravan[13]['Wert']):
                    Property_List_Taravan[18]['Wert'] = str(int(int(Property_List_Taravan[17]['Wert']) / 2))
                await message.channel.send('Taravan wird direkt getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[8:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Taravan[14]['Wert'] + '** LP und **' + Property_List_Taravan[16]['Wert'] + '** AP.')
        except:
            await message.channel.send('Ungültige Schadensangabe!')

#Command handling heavy damage dealt to any player. (Players can only inflict damage to self, while DM can inflict damage to any player.)
    elif message.content.startswith('!s. schaden'):
        try:
            Target_Damage = message.content[12:].lower()
            if Target_Damage.startswith('cloi') and DM_Status or Target_Damage.startswith('cloi') and str(message.author) == 'Echtgeilman92#2052':
                Schaden = int(Target_Damage[5:]) - int(Property_List_Cloi[12]['Wert'])
                if Schaden <= 0:
                    Schaden = 0
                Property_List_Cloi[14]['Wert'] = str(int(Property_List_Cloi[14]['Wert']) - Schaden)
                if int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]) < 0:
                    Property_List_Cloi[16]['Wert'] = '0'
                else:
                    Property_List_Cloi[16]['Wert'] = str(int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]))
                if int(Property_List_Cloi[14]['Wert']) * 2 < int(Property_List_Cloi[13]['Wert']) and int(Property_List_Cloi[16]['Wert']) > int(int(Property_List_Cloi[15]['Wert']) / 2):
                    Property_List_Cloi[16]['Wert'] = str(int(int(Property_List_Cloi[15]['Wert']) / 2))
                if int(Property_List_Cloi[14]['Wert']) * 2 < int(Property_List_Cloi[13]['Wert']):
                    Property_List_Cloi[18]['Wert'] = str(int(int(Property_List_Cloi[17]['Wert']) / 2))
                await message.channel.send('Cloi wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[5:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Cloi[14]['Wert'] + '** LP und **' + Property_List_Cloi[16]['Wert'] + '** AP.')
            elif Target_Damage.startswith('cordovan') and DM_Status or Target_Damage.startswith('cordovan') and str(message.author) == 'Aelron#6030':
                Schaden = int(Target_Damage[9:]) - int(Property_List_Cordovan[12]['Wert'])
                if Schaden <= 0:
                    Schaden = 0
                Property_List_Cordovan[14]['Wert'] = str(int(Property_List_Cordovan[14]['Wert']) - Schaden)
                if int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[9:]) < 0:
                    Property_List_Cordovan[16]['Wert'] = '0'
                else:
                    Property_List_Cordovan[16]['Wert'] = str(int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[9:]))
                if int(Property_List_Cordovan[14]['Wert']) * 2 < int(Property_List_Cordovan[13]['Wert']) and int(Property_List_Cordovan[16]['Wert']) > int(int(Property_List_Cordovan[15]['Wert']) / 2):
                    Property_List_Cordovan[16]['Wert'] = str(int(int(Property_List_Cordovan[15]['Wert']) / 2))
                if int(Property_List_Cordovan[14]['Wert']) * 2 < int(Property_List_Cordovan[13]['Wert']):
                    Property_List_Cordovan[18]['Wert'] = str(int(int(Property_List_Cordovan[17]['Wert']) / 2))
                await message.channel.send('Cordovan wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[9:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Cordovan[14]['Wert'] + '** LP und **' + Property_List_Cordovan[16]['Wert'] + '** AP.')
            elif Target_Damage.startswith('leonidas') and DM_Status or Target_Damage.startswith('leonidas') and str(message.author) == 'JohannesDberg#9702':
                Schaden = int(Target_Damage[9:]) - int(Property_List_Leonidas[12]['Wert'])
                if Schaden <= 0:
                    Schaden = 0
                Property_List_Leonidas[14]['Wert'] = str(int(Property_List_Leonidas[14]['Wert']) - Schaden)
                if int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[9:]) < 0:
                    Property_List_Leonidas[16]['Wert'] = '0'
                else:
                    Property_List_Leonidas[16]['Wert'] = str(int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[9:]))
                if int(Property_List_Leonidas[14]['Wert']) * 2 < int(Property_List_Leonidas[13]['Wert']) and int(Property_List_Leonidas[16]['Wert']) > int(int(Property_List_Leonidas[15]['Wert']) / 2):
                    Property_List_Leonidas[16]['Wert'] = str(int(int(Property_List_Leonidas[15]['Wert']) / 2))
                if int(Property_List_Leonidas[14]['Wert']) * 2 < int(Property_List_Leonidas[13]['Wert']):
                    Property_List_Leonidas[18]['Wert'] = str(int(int(Property_List_Leonidas[17]['Wert']) / 2))
                await message.channel.send('Leonidas wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[9:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Leonidas[14]['Wert'] + '** LP und **' + Property_List_Leonidas[16]['Wert'] + '** AP.')
            elif Target_Damage.startswith('taravan') and DM_Status or Target_Damage.startswith('taravan') and str(message.author) == 'Friedrich#6066':
                Schaden = int(Target_Damage[8:]) - int(Property_List_Taravan[12]['Wert'])
                if Schaden <= 0:
                    Schaden = 0
                Property_List_Taravan[14]['Wert'] = str(int(Property_List_Taravan[14]['Wert']) - Schaden)
                if int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[8:]) < 0:
                    Property_List_Taravan[16]['Wert'] = '0'
                else:
                    Property_List_Taravan[16]['Wert'] = str(int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[8:]))
                if int(Property_List_Taravan[14]['Wert']) * 2 < int(Property_List_Taravan[13]['Wert']) and int(Property_List_Taravan[16]['Wert']) > int(int(Property_List_Taravan[15]['Wert']) / 2):
                    Property_List_Taravan[16]['Wert'] = str(int(int(Property_List_Taravan[15]['Wert']) / 2))
                if int(Property_List_Taravan[14]['Wert']) * 2 < int(Property_List_Taravan[13]['Wert']):
                    Property_List_Taravan[18]['Wert'] = str(int(int(Property_List_Taravan[17]['Wert']) / 2))
                await message.channel.send('Taravan wird schwer getroffen und nimmt ' + str(Schaden) + ' schweren und ' + Target_Damage[8:] + ' leichten Schaden.\nEr hat jetzt noch **' + Property_List_Taravan[14]['Wert'] + '** LP und **' + Property_List_Taravan[16]['Wert'] + '** AP.')
        except:
            await message.channel.send('Ungültige Schadensangabe!')

#Command handling light damage dealt to any player. (Players can only inflict damage to self, while DM can inflict damage to any player.)
    elif message.content.startswith('!l. schaden'):
        try:
            Target_Damage = message.content[12:].lower()
            if Target_Damage.startswith('cloi') and DM_Status or Target_Damage.startswith('cloi') and str(message.author) == 'Echtgeilman92#2052':
                if int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]) < 0:
                    Property_List_Cloi[16]['Wert'] = '0'
                else:
                    Property_List_Cloi[16]['Wert'] = str(int(Property_List_Cloi[16]['Wert']) - int(Target_Damage[5:]))
                await message.channel.send('Cloi nimmt ' + str(Target_Damage[5:]) + ' leichten Schaden.\nEr hat jetzt noch **' + str(Property_List_Cloi[16]['Wert']) + '** AP.')
            if Target_Damage.startswith('cordovan') and DM_Status or Target_Damage.startswith('cordovan') and str(message.author) == 'Aelron#6030':
                if int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[9:]) < 0:
                    Property_List_Cordovan[16]['Wert'] = '0'
                else:
                    Property_List_Cordovan[16]['Wert'] = str(int(Property_List_Cordovan[16]['Wert']) - int(Target_Damage[9:]))
                await message.channel.send('Cordovan nimmt ' + str(Target_Damage[9:]) + ' leichten Schaden.\nEr hat jetzt noch **' + str(Property_List_Cordovan[16]['Wert']) + '** AP.')
            if Target_Damage.startswith('leonidas') and DM_Status or Target_Damage.startswith('leonidas') and str(message.author) == 'JohannesDberg#9702':
                if int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[9:]) < 0:
                    Property_List_Leonidas[16]['Wert'] = '0'
                else:
                    Property_List_Leonidas[16]['Wert'] = str(int(Property_List_Leonidas[16]['Wert']) - int(Target_Damage[9:]))
                await message.channel.send('Leonidas nimmt ' + str(Target_Damage[9:]) + ' leichten Schaden.\nEr hat jetzt noch **' + str(Property_List_Leonidas[16]['Wert']) + '** AP.')
            if Target_Damage.startswith('taravan') and DM_Status or Target_Damage.startswith('taravan') and str(message.author) == 'Friedrich#6066':
                if int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[8:]) < 0:
                    Property_List_Taravan[16]['Wert'] = '0'
                else:
                    Property_List_Taravan[16]['Wert'] = str(int(Property_List_Taravan[16]['Wert']) - int(Target_Damage[8:]))
                await message.channel.send('Taravan nimmt ' + str(Target_Damage[8:]) + ' leichten Schaden.\nEr hat jetzt noch **' + str(Property_List_Taravan[16]['Wert']) + '** AP.')
        except:
            await message.channel.send('Ungültige Schadensangabe!')

#Command handling fall damage calculations.
    elif message.content.lower().startswith('!fallschaden'):
        try:
            height = message.content[13:]
            if int(height) > 100:
                await message.channel.send('Tod')
            elif int(height) < 2:
                await message.channel.send('Kein Fallschaden aus dieser Höhe möglich.')
            elif int(height) == 2:
                if random.randint(1,100) >= int(Current_Property_Set[1]['Wert']):
                    await message.channel.send('Du fällst und nimmst **' + str(random.randint(1,6)) + '** (1W6)' + ' AP Schaden!')
                else:
                    await message.channel.send('Du fällst und nimmst **' + str(random.randint(1,6)) + '** (1W6)' + ' LP und AP Schaden!')
            else:
                if (int(height) % 2) == 1:
                    damage = 0
                    for i in range(int((int(height) - 1) / 2)):
                        damage += random.randint(1, 6)
                    await message.channel.send('Du fällst und nimmst **' + str(damage + 2) + '** (' + str(int((int(height) - 1) / 2)) + 'W6+2)' + ' LP und AP Schaden')
                else:
                    damage = 0
                    for i in range(int(int(height) / 2)):
                        damage += random.randint(1, 6)
                    await message.channel.send('Du fällst und nimmst **' + str(damage) + '** (' + str(int((int(height) - 1) / 2)) + 'W6)' + ' LP und AP Schaden')
            if int(height) >= 6:
                response = 'Zusätzlich tritt folgender Effekt auf Grund der hohen Fallhöhe ein:'
                roll = random.randint(1,100)
                if roll >= 91 and roll <= 100:
                    roll = random.randint(11,91)
                    for i in range(len(Fall_Damage_Effects)):
                        if int(Fall_Damage_Effects[i]['Wert']) <= roll:
                            Effekt_Ausgabe1 = umlaute(Fall_Damage_Effects[i]['Effekt'])
                        else:
                            break
                    while True:
                        roll = random.randint(11,91)
                        for i in range(len(Fall_Damage_Effects)):
                            if int(Fall_Damage_Effects[i]['Wert']) <= roll:
                                Effekt_Ausgabe2 = umlaute(Fall_Damage_Effects[i]['Effekt'])
                            else:
                                break
                        if Effekt_Ausgabe1 != Effekt_Ausgabe2:
                            break
                    response = response + '\n**Zwei Effekte:**\n' + Effekt_Ausgabe1 + '\n' + Effekt_Ausgabe2
                else:
                    for i in range(len(Fall_Damage_Effects)):
                        if int(Fall_Damage_Effects[i]['Wert']) <= roll:
                            Effekt_Ausgabe = umlaute(Fall_Damage_Effects[i]['Effekt'])
                        else:
                            break
                    response = response + '\n' + Effekt_Ausgabe
                await message.channel.send(response)
        except:
            await message.channel.send('Ungültige Fallhöhe')

#Command for changing armor class.
    elif message.content.lower().startswith('!rüstung'):
        try:
            rüstung = int(message.content[9:])
            if str(message.author) == 'Echtgeilman92#2052':
                Changes = armor_changes(Property_List_Cloi, rüstung, Ability_List_Cloi)
                Property_List_Cloi[12]['Wert'] = str(Changes[0])
                Property_List_Cloi[9]['Wert'] = Changes[1]
                Property_List_Cloi[18]['Wert'] = Changes[2]
                await message.channel.send(Changes[3])
            elif str(message.author) == 'Aelron#6030':
                Changes = armor_changes(Property_List_Cordovan, rüstung, Ability_List_Cordovan)
                Property_List_Cordovan[12]['Wert'] = str(Changes[0])
                Property_List_Cordovan[9]['Wert'] = Changes[1]
                Property_List_Cordovan[18]['Wert'] = Changes[2]
                await message.channel.send(Changes[3])
            elif str(message.author) == 'JohannesDberg#9702':
                Changes = armor_changes(Property_List_Leonidas, rüstung, Ability_List_Leonidas)
                Property_List_Leonidas[12]['Wert'] = str(Changes[0])
                Property_List_Leonidas[9]['Wert'] = Changes[1]
                Property_List_Leonidas[18]['Wert'] = Changes[2]
                await message.channel.send(Changes[3])
            elif str(message.author) == 'Friedrich#6066' or str(message.author) == 'Ponk#0213':
                Changes = armor_changes(Property_List_Taravan, rüstung, Ability_List_Taravan)
                Property_List_Taravan[12]['Wert'] = str(Changes[0])
                Property_List_Taravan[9]['Wert'] = Changes[1]
                Property_List_Taravan[18]['Wert'] = Changes[2]
                await message.channel.send(Changes[3])
        except:
            await message.channel.send('Ungültige Eingabe')

#Command listing character stats.
    elif message.content.lower() == '!stats':
        output = '**Deine Stats:**\n```LP:' + Current_Property_Set[14]['Wert'] + '/' + Current_Property_Set[13]['Wert']
        output = output + '   AP:' + Current_Property_Set[16]['Wert'] + '/' + Current_Property_Set[15]['Wert'] + '   Bewegungsweite:' + Current_Property_Set[18]['Wert'] + '/' + Current_Property_Set[17]['Wert']
        output = output + '   Rüstung:' + Current_Property_Set[12]['Wert'] + '\n' + 'Stärke:' + Current_Property_Set[4]['Wert'] + ' Geschicklichkeit:' + Current_Property_Set[0]['Wert'] 
        output = output + ' Gewandheit:' + Current_Property_Set[1]['Wert'] + ' Konstitution:' + Current_Property_Set[2]['Wert'] + ' Intelligenz:' + Current_Property_Set[3]['Wert'] + '\nZaubertalent:' + Current_Property_Set[5]['Wert']
        output = output + ' Aussehen:' + Current_Property_Set[7]['Wert'] + ' Persönliche Ausstrahlung:' + Current_Property_Set[6]['Wert'] + ' Willenskraft:' + Current_Property_Set[8]['Wert'] + '```'
        await message.channel.send(output)

#Command listing currently available weapons of the players.
    elif message.content.lower() == '!waffen':
        output = 'Waffen, die momentan zur Verfügung stehen:\n```'
        for i in range(len(Current_Attack_Set)):
            output = output + umlaute(Current_Attack_Set[i]['Name']) + ' (' + Current_Attack_Set[i]['Grundschaden'] + 'W6+' + str(damage_bonus(Current_Property_Set)+int(Current_Attack_Set[i]['Magischer Schadensbonus'])) + ' Schaden) mit Angriff von +' + str(int(Current_Attack_Set[i]['Fertigkeitswert']) + int(Current_Attack_Set[i]['Magischer Angriffsbonus']) + attack_bonus(Current_Property_Set, Current_Ability_Set[24]['Wert'], Current_Attack_Set[i])) + '\n'
        await message.channel.send(output + '```')

#Command listing currently available spells of the players.
    elif message.content.lower() == '!zauber':
        if len(Current_Spell_List) == 0:
            await channel.message.send('Du erinnerst dich plötzlich, dass du keine Ahnung von Magie hast.')
        else:
            output = 'Die Zauber die dir zur Verfügung stehen sind:\n```'
            for i in range(len(Current_Spell_List)):
                output = output + umlaute(Current_Spell_List[i]['Name']) + '\n'
            await message.channel.send(output + '```Für weitere Information benutze **!info + Zaubername**')

#Command giving info on individual items like spells and items.
    elif message.content.lower().startswith('!info'):
        item = message.content[6:].lower()
        if item == 'zaubername':
            await message.channel.send('https://i.imgflip.com/3kk1hj.jpg')
        else:
            for i in range(len(Spell_List)):
                if umlaute(Spell_List[i]['Name'].lower()) == item:
                    await message.channel.send(umlaute('```' + item.capitalize() + ' (' + Spell_List[i]['Methode'] + ' aus der Schule der ' + Spell_List[i]['Schule'] + ')\n\n' + 'AP-Verbrauch: ' + Spell_List[i]['AP-Verbrauch'] + '\nZauberdauer: ' + Spell_List[i]['Zauberdauer'] + '\nReichweite: ' + Spell_List[i]['Reichweite'] + '\nWirkungsziel: ' + Spell_List[i]['Wirkungsziel'] + '\nWirkungsbereich: ' + Spell_List[i]['Wirkungsbereich'] + '\nWirkungsdauer: ' + Spell_List[i]['Wirkungsdauer'] + '\nUrsprung: ' + Spell_List[i]['Ursprung'] + '\n\n' + Spell_List[i]['Effekt'] + '```'))
                    break

#Command rolling a random dice.
    elif message.content.lower().startswith('!w '):
        Number = message.content[3:]
        try:
            await message.channel.send('**' + str(random.randint(1, int(Number))) + '**')
        except:
            await message.channel.send('https://i.imgflip.com/3kk1hj.jpg')
    elif message.content.lower().startswith('!w'):
        Number = message.content[2:]
        try:
            await message.channel.send('**' + str(random.randint(1, int(Number))) + '**')
        except:
            await message.channel.send('https://i.imgflip.com/3kk1hj.jpg')

#Command for showing all the commands.
    # elif message.content == '!commands':
    #     await message.channel.send('h')

#Command for playing youtube videos.
    # elif message.content == '!play':
    #     server = ctx.message.server
    #     voice_client = client.voice_client_in(server)
    #     player = await voice_client.create_ytdl_player(url)
    #     players[server.id] = player
    #     player.start()

#Command for playing youtube videos.
    # elif message.content == '!join' and DM_Status:
    #     channel = message.author.voice.channel
    #     await channel.connect()

###----------------------------------------------------
#Commands for the DM to observe and controll gameplay
###----------------------------------------------------

#Command for loading gamedata.
    elif message.content == '!load game' and DM_Status:
        load_game_data()
        await message.channel.send('**Spieldateien erfolgreich geladen!**')

#Command for loading character data.
    elif message.content == '!load characters' and DM_Status:
        load_character_data()
        await message.channel.send('**Characterdateien erfolgreich geladen!**')

#Command for saving the game (Updating all the values of the property file to the according .json files)
    elif message.content == '!save':
        save_data()
        await message.channel.send('**Spiel erfolgreich gespeichert!**')

#Command for requesting information on critical injuries.
    elif message.content.startswith('!effekt') and DM_Status:
        injury = message.content[8:].lower()
        for i in range(len(Injury_List)):
            if umlaute(Injury_List[i]['Name']).lower() == injury:
                await message.channel.send('```' + umlaute(Injury_List[i]['Effekt']) + '```')
                break

#Command for requesting specific crit effects without having to do an according roll.
    elif message.content.startswith('!crit') and DM_Status:
        try:
            Request = message.content[6:]
            if Request.startswith('fail attack'):
                for i in range(len(Crit_Fails_Attack)):
                    if int(Crit_Fails_Attack[i]['Wert']) <= int(Request[12:]):
                        Effekt_Ausgabe = Crit_Fails_Attack[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('success attack'):
                for i in range(len(Crit_Success_Attack)):
                    if int(Crit_Success_Attack[i]['Wert']) <= int(Request[15:]):
                        Effekt_Ausgabe = Crit_Success_Attack[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('fail defense'):
                for i in range(len(Crit_Fails_Defense)):
                    if int(Crit_Fails_Defense[i]['Wert']) <= int(Request[13:]):
                        Effekt_Ausgabe = Crit_Fails_Defense[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('success defense'):
                for i in range(len(Crit_Success_Defense)):
                    if int(Crit_Success_Defense[i]['Wert']) <= int(Request[16:]):
                        Effekt_Ausgabe = Crit_Success_Defense[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
            elif Request.startswith('fail spells'):
                for i in range(len(Crit_Fails_Spells)):
                    if int(Crit_Fails_Spells[i]['Wert']) <= int(Request[12:]):
                        Effekt_Ausgabe = Crit_Fails_Spells[i]['Effekt']
                    else:
                        break
                await message.channel.send(umlaute(Effekt_Ausgabe))
        except:
            await message.channel.send('Ungültige Anfrage')

#Command handling healing of AP and LP damage.
    elif message.content.lower().startswith('!heilung') and DM_Status:
        try:
            Target_Heal = message.content[9:].lower()
            if Target_Heal.startswith('cloi'):
                Heal_Amount = int(Target_Heal[8:])
                if Target_Heal[5:].startswith('ap'):
                    New_AP = int(Property_List_Cloi[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Cloi[15]['Wert']):
                        New_AP = Property_List_Cloi[15]['Wert']
                    if int(Property_List_Cloi[14]['Wert']) < (int(Property_List_Cloi[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Cloi[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Cloi[15]['Wert']) / 2)
                    Property_List_Cloi[16]['Wert'] = str(New_AP)
                    await message.channel.send('Cloi heilt ' + str(Heal_Amount) + ' AP.\nEr hat jetzt **' + str(Property_List_Cloi[16]['Wert']) + '** AP.')
                elif Target_Heal[5:].startswith('lp'):
                    New_LP = int(Property_List_Cloi[14]['Wert']) + Heal_Amount
                    if New_LP > int(Property_List_Cloi[13]['Wert']):
                        New_LP = Property_List_Cloi[13]['Wert']
                    Property_List_Cloi[14]['Wert'] = str(New_LP)
                    if int(Property_List_Cloi[14]['Wert']) * 2 >= int(Property_List_Cloi[13]['Wert']):
                        Property_List_Cloi[18]['Wert'] = Property_List_Cloi[17]['Wert']
                    New_AP = int(Property_List_Cloi[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Cloi[15]['Wert']):
                        New_AP = Property_List_Cloi[15]['Wert']
                    if int(Property_List_Cloi[14]['Wert']) < (int(Property_List_Cloi[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Cloi[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Cloi[15]['Wert']) / 2)
                    Property_List_Cloi[16]['Wert'] = str(New_AP)
                    await message.channel.send('Cloi heilt ' + str(Heal_Amount) + ' und AP.\nEr hat jetzt **' + Property_List_Cloi[14]['Wert'] + '** LP und **' + Property_List_Cloi[16]['Wert'] + '** AP.')
            elif Target_Heal.startswith('cordovan'):
                Heal_Amount = int(Target_Heal[12:])
                if Target_Heal[9:].startswith('ap'):
                    New_AP = int(Property_List_Cordovan[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Cordovan[15]['Wert']):
                        New_AP = Property_List_Cordovan[15]['Wert']
                    if int(Property_List_Cordovan[14]['Wert']) < (int(Property_List_Cordovan[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Cordovan[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Cordovan[15]['Wert']) / 2)
                    Property_List_Cordovan[16]['Wert'] = str(New_AP)
                    await message.channel.send('Cordovan heilt ' + str(Heal_Amount) + ' AP.\nEr hat jetzt **' + str(Property_List_Cordovan[16]['Wert']) + '** AP.')
                elif Target_Heal[9:].startswith('lp'):
                    New_LP = int(Property_List_Cordovan[14]['Wert']) + Heal_Amount
                    if New_LP > int(Property_List_Cordovan[13]['Wert']):
                        New_LP = Property_List_Cordovan[13]['Wert']
                    Property_List_Cordovan[14]['Wert'] = str(New_LP)
                    if int(Property_List_Cordovan[14]['Wert']) * 2 >= int(Property_List_Cordovan[13]['Wert']):
                        Property_List_Cordovan[18]['Wert'] = Property_List_Cordovan[17]['Wert']
                    New_AP = int(Property_List_Cordovan[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Cordovan[15]['Wert']):
                        New_AP = Property_List_Cordovan[15]['Wert']
                    if int(Property_List_Cordovan[14]['Wert']) < (int(Property_List_Cordovan[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Cordovan[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Cordovan[15]['Wert']) / 2)
                    Property_List_Cordovan[16]['Wert'] = str(New_AP)
                    await message.channel.send('Cordovan heilt ' + str(Heal_Amount) + ' und AP.\nEr hat jetzt **' + Property_List_Cordovan[14]['Wert'] + '** LP und **' + Property_List_Cordovan[16]['Wert'] + '** AP.')
            elif Target_Heal.startswith('leonidas'):
                Heal_Amount = int(Target_Heal[12:])
                if Target_Heal[9:].startswith('ap'):
                    New_AP = int(Property_List_Leonidas[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Leonidas[15]['Wert']):
                        New_AP = Property_List_Leonidas[15]['Wert']
                    if int(Property_List_Leonidas[14]['Wert']) < (int(Property_List_Leonidas[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Leonidas[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Leonidas[15]['Wert']) / 2)
                    Property_List_Leonidas[16]['Wert'] = str(New_AP)
                    await message.channel.send('Leonidas heilt ' + str(Heal_Amount) + ' AP.\nEr hat jetzt **' + str(Property_List_Leonidas[16]['Wert']) + '** AP.')
                elif Target_Heal[9:].startswith('lp'):
                    New_LP = int(Property_List_Leonidas[14]['Wert']) + Heal_Amount
                    if New_LP > int(Property_List_Leonidas[13]['Wert']):
                        New_LP = Property_List_Leonidas[13]['Wert']
                    Property_List_Leonidas[14]['Wert'] = str(New_LP)
                    if int(Property_List_Leonidas[14]['Wert']) * 2 >= int(Property_List_Leonidas[13]['Wert']):
                        Property_List_Leonidas[18]['Wert'] = Property_List_Leonidas[17]['Wert']
                    New_AP = int(Property_List_Leonidas[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Leonidas[15]['Wert']):
                        New_AP = Property_List_Leonidas[15]['Wert']
                    if int(Property_List_Leonidas[14]['Wert']) < (int(Property_List_Leonidas[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Leonidas[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Leonidas[15]['Wert']) / 2)
                    Property_List_Leonidas[16]['Wert'] = str(New_AP)
                    await message.channel.send('Leonidas heilt ' + str(Heal_Amount) + ' und AP.\nEr hat jetzt **' + Property_List_Leonidas[14]['Wert'] + '** LP und **' + Property_List_Leonidas[16]['Wert'] + '** AP.')
            elif Target_Heal.startswith('taravan'):
                Heal_Amount = int(Target_Heal[11:])
                if Target_Heal[8:].startswith('ap'):
                    New_AP = int(Property_List_Taravan[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Taravan[15]['Wert']):
                        New_AP = Property_List_Taravan[15]['Wert']
                    if int(Property_List_Taravan[14]['Wert']) < (int(Property_List_Taravan[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Taravan[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Taravan[15]['Wert']) / 2)
                    Property_List_Taravan[16]['Wert'] = str(New_AP)
                    await message.channel.send('Taravan heilt ' + str(Heal_Amount) + ' AP.\nEr hat jetzt **' + str(Property_List_Taravan[16]['Wert']) + '** AP.')
                elif Target_Heal[8:].startswith('lp'):
                    New_LP = int(Property_List_Taravan[14]['Wert']) + Heal_Amount
                    if New_LP > int(Property_List_Taravan[13]['Wert']):
                        New_LP = Property_List_Taravan[13]['Wert']
                    Property_List_Taravan[14]['Wert'] = str(New_LP)
                    if int(Property_List_Taravan[14]['Wert']) * 2 >= int(Property_List_Taravan[13]['Wert']):
                        Property_List_Taravan[18]['Wert'] = Property_List_Taravan[17]['Wert']
                    New_AP = int(Property_List_Taravan[16]['Wert']) + Heal_Amount
                    if New_AP > int(Property_List_Taravan[15]['Wert']):
                        New_AP = Property_List_Taravan[15]['Wert']
                    if int(Property_List_Taravan[14]['Wert']) < (int(Property_List_Taravan[13]['Wert']) / 2) and int(New_AP) > (int(Property_List_Taravan[16]['Wert']) / 2):
                        New_AP = int(int(Property_List_Taravan[15]['Wert']) / 2)
                    Property_List_Taravan[16]['Wert'] = str(New_AP)
                    await message.channel.send('Taravan heilt ' + str(Heal_Amount) + ' und AP.\nEr hat jetzt **' + Property_List_Taravan[14]['Wert'] + '** LP und **' + Property_List_Taravan[16]['Wert'] + '** AP.')
        except:
            await message.channel.send('Ungültige Angabe!')

#Command for giving every player 1LP after midnight.
    elif message.content.lower() == '!mitternacht' and DM_Status:
        try:
            New_LP = int(Property_List_Cloi[14]['Wert']) + 1
            if New_LP > int(Property_List_Cloi[13]['Wert']):
                New_LP = Property_List_Cloi[13]['Wert']
            Property_List_Cloi[14]['Wert'] = str(New_LP)
            if int(Property_List_Cloi[14]['Wert']) * 2 >= int(Property_List_Cloi[13]['Wert']):
                Property_List_Cloi[18]['Wert'] = Property_List_Cloi[17]['Wert']
            New_LP = int(Property_List_Cordovan[14]['Wert']) + 1
            if New_LP > int(Property_List_Cordovan[13]['Wert']):
                New_LP = Property_List_Cordovan[13]['Wert']
            Property_List_Cordovan[14]['Wert'] = str(New_LP)
            if int(Property_List_Cordovan[14]['Wert']) * 2 >= int(Property_List_Cordovan[13]['Wert']):
                Property_List_Cordovan[18]['Wert'] = Property_List_Cordovan[17]['Wert']
            New_LP = int(Property_List_Leonidas[14]['Wert']) + 1
            if New_LP > int(Property_List_Leonidas[13]['Wert']):
                New_LP = Property_List_Leonidas[13]['Wert']
            Property_List_Leonidas[14]['Wert'] = str(New_LP)
            if int(Property_List_Leonidas[14]['Wert']) * 2 >= int(Property_List_Leonidas[13]['Wert']):
                Property_List_Leonidas[18]['Wert'] = Property_List_Leonidas[17]['Wert']
            New_LP = int(Property_List_Taravan[14]['Wert']) + 1
            if New_LP > int(Property_List_Taravan[13]['Wert']):
                New_LP = Property_List_Taravan[13]['Wert']
            Property_List_Taravan[14]['Wert'] = str(New_LP)
            if int(Property_List_Taravan[14]['Wert']) * 2 >= int(Property_List_Taravan[13]['Wert']):
                Property_List_Taravan[18]['Wert'] = Property_List_Taravan[17]['Wert']
            await message.channel.send('Alle erhalten einen LP wieder.')
        except:
            await message.channel.send('Die Sonne will einfach nicht untergehen...')

with open('Token/Discord_Token.txt', 'r') as file:
    Token = file.read()
players = {}
client.run(Token)