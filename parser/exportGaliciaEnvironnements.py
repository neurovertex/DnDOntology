__author__ = 'benji'

# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pylab as pl
import numpy as np

tree = ET.parse('database-en.xml')
root = tree.getroot()

monstres = []
types = ["Beast", "Construct", "Magical", "Aberration", "Colossal", "Elemental", "Ooze", "Dragon", "Humanoid", "Outsider", "Vermin", "Fey", "Monstrous", "Undead", "Giant", "Animal", "Plant"]
tailles = ["Fine", "Small", "Medium", "Large", "Huge", "Gargantuan", "Colossal"]
facteurs = ["Dés_De_Vie", "Initiative", "Puissance"]
facteurs_xml = ["dv", "init", "puiss"]
seuilsFacteurs = [(30, 80, 151), (0, 2, 5), 10]
classesCaracFacteur1 = ["faible", "moyen", "élevé", "très élevé"]
classesCaracFacteur2 = ["malus", "faible", "moyen", "élevé"]
classesCaracFacteur3 = ["faible", "élevé"]
classeArmure = ["Classe_D'Armure"]
classeArmure_xml = ["ca"]
seuilsArmure = [(0, 7, 12)]
classesCaracArmure = ["malus", "faible", "moyen", "élevé"]
attaqueBase = ["Attaque de Base"]
attaqueBase_xml = ["bba"]
seuilsAttaqueBase = [8]
classesCaracAttaqueBase = ["faible", "élevé"]
attaqueLutte = ["Attaque de Lutte"]
attaqueLutte_xml = ["bba"]
seuilsAttaqueLutte = [(0, 11, 21)]
classesCaracAttaqueLutte = ["malus", "faible", "moyen", "élevé"]
alignements = ["loyal", "neutral", "chaotic", "good", "evil"]
environnements = ["A neutral evil plane", "Plane of Shadow", "A chaotic-aligned plane", "Underground", "Warm plains", "Cold marshes", "An evil-aligned plane", "mountains", "Temperate marshes (Pyro: Warm marshes) (Cryo: Cold marshes)", "Cold desert", "Any temperate or cold land", "Warm forest", "Temperate hills (Forest gnomes: Temperate forests)", "A lawful evil-aligned plane", "Cold aquatic", "Elemental Plane of Water", "Any land and underground", "Temperate forest(Half-elf: Temperate forests)(Aquatic: Temperate aquatic)(Gray: Temperate mountains)(Wild: Warm forests)(Wood: Temperate forests)", "Warm mountains", "Temperate mountains (Deep: Underground)", "underground", "Warm aquatic", "Warm deserts", "Cold mountains", "Temperate mountains", "A good-aligned plane.", "Temperate deserts", "Cold plains", "A lawful-aligned plane", "A chaotic good-aligned plane", "Any good-aligned plane", "Temperate plains", "A chaotic evil-aligned plane", "Temperate forests", "Temperate hills", "Chaotic evil-Aligned planes", "Any forest", "A chaotic evil-Aligned plane", "Cold hills", "Temperate marshes", "A chaotic good plane", "Temperate aquatic", "Any sunny land", "Temperate marshes(Pyro: Warm marshes)(Cryo: Cold marshes)", "Warm hills", "Warm desert", "Temperate marshes(Pyro: Warm marshes) (Cryo: Cold marshes)", "Elemental Plane of Air", "A lawful good-aligned plane", "Elemental Plane of Fire", "plains", "Any aquatic", "A lawful evil plane", "A evil-aligned plane", "Any cold", "Any land", "Ethereal Plane", "Any urban", "Warm plains(Deep halfling: Warm hills)(Tallfellow: Temperate forests)", "Cold forests", "Warm marshes", "Any", "Temperate forest", "Warm forests", "Elemental Plane of Earth", "hill", "Positive Energy Plane", "Chaotic-Aligned Plane", "A lawful good plane"]
environnementsToWrite = ["Underground", "Plain", "Hill", "Forests", "Aquatic", "Marsh", "Mountain", "Desert", "Urban", "Plane", "Warm", "Temperate", "Cold", "Sunny", "Loyalty Chaotic", "Loyalty Neutral", "Loyalty Lawful", "Morality Positive(good)", "Morality Evil", "Elemental_Earth", "Elemental_Fire", "Elemental_Water", "Elemental_Air", "Shadow", "Ethereal"]
jetsSauvegardes = ["Réflexe", "Vigueur", "Volonté"]
jetsSauvegardes_xml = ["Fort", "Ref", "Will"]
seuilsJetsSauvegardes = [9, 8, 6]
classesCaracJetsSauvegardes = ["faible", "fort"]
caracs = ["Force", "Dexterite", "Consistance", "Intelligence", "Sagesse", "Charisme"]
caracs_xml = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
seuilsCarac = [(12, 22), 14, 18, (9, 20), (2, 15), (8, 16)]
classesCarac1 = ["faible", "moyen", "élevé"]
classesCarac2 = ["faible", "élevé"]
classesCarac3 = ["inexistant", "faible", "élevé"]
classesCarac4 = ["inexistant", "faible", "moyen", "élevé"]
classesCarac5 = ["inexistant", "faible", "élevé"]
classesCarac6 = ["faible", "moyen", "élevé"]
classesCarac = ["faible", "moyen", "élevé"]

decalages = []
resultsCarac = []

for num_monstre, monstre in enumerate(root):
    monstres.append(monstre.find('name').text.strip())

    décalage = 0
    attr_node = monstre.find('type')
    if attr_node != None:
        val = attr_node.text.strip()
        if val:
            val = val.lower()
            for num_attr, attrname in enumerate(types):
                if val == attrname.lower():
                    resultsCarac.append((num_monstre, num_attr))
                    break

    décalage += len(types)
    decalages.append(décalage)
    attr_node = monstre.find('taille')
    if attr_node != None:
        val = attr_node.text.strip()
        if val:
            for num_attr, attrname in enumerate(tailles):
                if attrname == "Fine":
                    if val == attrname or val == "Diminutive" or val == "Tiny":
                        resultsCarac.append((num_monstre, décalage + num_attr))
                        break
                if val == attrname:
                    resultsCarac.append((num_monstre, décalage + num_attr))
                    break

    décalage += len(tailles)
    decalages.append(décalage)
    for num_attr, attrname in enumerate(facteurs_xml):
        seuil = seuilsFacteurs[num_attr]
        attr_node = monstre.find(attrname)
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                if num_attr == 0:
                    if '(' in val:
                        machin, val = val.split("(",1)
                    if 'hp' in val:
                        val, machin = val.split("hp",1)
                    val = val.strip()
                    if ',' in val:
                        val1, val2 = val.split(",",1)
                        val = val1 + val2
                        val = val.strip()
                    score = 0
                    val = int(val)
                    if val < seuil[0]:
                       score = 0
                    elif seuil[0] <= val < seuil[1]:
                        score = 1
                    elif seuil[1] <= val < seuil[2]:
                        score = 2
                    else:
                        score = 3
                    resultsCarac.append((num_monstre, décalage + 4 * num_attr + score))
                if num_attr == 1:
                    if '(' in val:
                        val, machin = val.split("(",1)
                    if '+' in val:
                        machin, val = val.split("+",1)
                    #On fait la somme des 2 init
                    if '+' in val:
                        val, machin = val.split("+",1)
                    #    sum1, sum2 = val.split("+",1)
                    #    val = int(sum1) + int(sum2)
                    score = 0
                    val = int(val)
                    if val < seuil[0]:
                        score = 0
                    elif seuil[0] <= val < seuil[1]:
                        score = 1
                    elif seuil[1] <= val < seuil[2]:
                        score = 2
                    else:
                        score = 3
                    resultsCarac.append((num_monstre, décalage + 4 * num_attr + score))
                if num_attr == 2:
                    if '(' in val:
                        val, machin = val.split("(",1)
                    score = 0
                    if '/' in val:
                        numerateur, denominateur = val.split("/")
                        val = float(float(numerateur) / float(denominateur))
                    else:
                        val = int(val)
                    if val < seuil:
                        score = 0
                    else:
                        score = 1
                    resultsCarac.append((num_monstre, décalage + 4 * num_attr + score))

    décalage +=  len(classesCaracFacteur1) + len(classesCaracFacteur2) + len(classesCaracFacteur3)
    decalages.append(décalage)
    for num_attr, attrname in enumerate(classeArmure_xml):
        seuil = seuilsArmure[num_attr]
        attr_node = monstre.find('ca/bonus[@class="naturelle"]')
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                if '+' in val:
                    machin, val = val.split("+")
                score = 0
                val = int(val)
                if val < seuil[0]:
                    score = 0
                elif seuil[0] <= val < seuil[1]:
                    score = 1
                elif seuil[1] <= val < seuil[2]:
                    score = 2
                else:
                    score = 3
                resultsCarac.append((num_monstre, décalage + 4 * num_attr + score))

    décalage += len(classesCaracArmure)
    decalages.append(décalage)
    for num_attr, attrname in enumerate(attaqueBase_xml):
        seuil = seuilsAttaqueBase[num_attr]
        attr_node = monstre.find('bba/base')
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                if '+' in val:
                    machin, val = val.split("+")
                score = 0
                val = int(val)
                if val < seuil:
                    score = 0
                else:
                    score = 1
                resultsCarac.append((num_monstre, décalage + 2 * num_attr + score))

    décalage += len(classesCaracAttaqueBase)
    decalages.append(décalage)
    for num_attr, attrname in enumerate(attaqueLutte_xml):
        seuil = seuilsAttaqueLutte[num_attr]
        attr_node = monstre.find('bba/lutte')
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                if '*' in val:
                    val, machin = val.split("*")
                if 'w' in val:
                    val, machin = val.split("w")
                if '+' in val:
                    machin, val = val.split("+",1)
                #On fait la somme des 2 attaques de luttes
                if '+' in val:
                    val, machin = val.split("+",1)
                #    sum1, sum2 = val.split("+",1)
                #    val = int(sum1) + int(sum2)
                score = 0
                if '-' == val:
                    score = 0
                else:
                    val = int(val)
                    if val < seuil[0]:
                        score = 0
                    elif seuil[0] <= val < seuil[1]:
                        score = 1
                    elif seuil[1] <= val < seuil[2]:
                        score = 2
                    else:
                        score = 3
                resultsCarac.append((num_monstre, décalage + 4 * num_attr + score))

    décalage += len(classesCaracAttaqueLutte)
    decalages.append(décalage)
    for num_node, attr_node in enumerate(monstre.findall('align')):
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                for num_attr, attrname in enumerate(alignements):
                    if val == attrname:
                        resultsCarac.append((num_monstre, décalage + num_attr))
                        break

    décalage += (num_node + 1) * len(alignements)
    decalages.append(décalage)
    attr_node = monstre.find('environ')
    if attr_node != None:
        val = attr_node.text.strip()
        if val:
            for num_attr, attrname in enumerate(environnements):
                if val == attrname:
                    print(num_attr)
                    #resultsCarac.append((num_monstre, décalage + num_attr))
                    if num_attr == 0:
                        resultsCarac.append((num_monstre, décalage + 15))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 1:
                        resultsCarac.append((num_monstre, décalage + 23))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 2:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 3:
                        resultsCarac.append((num_monstre, décalage + 0))
                        break
                    if num_attr == 4:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 1))
                        break
                    if num_attr == 5:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 5))
                        break
                    if num_attr == 6:
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 7:
                        resultsCarac.append((num_monstre, décalage + 6))
                        break
                    if num_attr == 8:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 5))
                        break
                    if num_attr == 9:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 7))
                        break
                    if num_attr == 10:
                        resultsCarac.append((num_monstre, décalage + 0))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 3))
                        resultsCarac.append((num_monstre, décalage + 4))
                        resultsCarac.append((num_monstre, décalage + 5))
                        resultsCarac.append((num_monstre, décalage + 6))
                        resultsCarac.append((num_monstre, décalage + 7))
                        resultsCarac.append((num_monstre, décalage + 8))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 12))
                        break
                    if num_attr == 11:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 12:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 2))
                        break
                    if num_attr == 13:
                        resultsCarac.append((num_monstre, décalage + 16))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 14:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 4))
                        break
                    if num_attr == 15:
                        resultsCarac.append((num_monstre, décalage + 21))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 16:
                        resultsCarac.append((num_monstre, décalage + 0))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 3))
                        resultsCarac.append((num_monstre, décalage + 5))
                        resultsCarac.append((num_monstre, décalage + 6))
                        resultsCarac.append((num_monstre, décalage + 7))
                        resultsCarac.append((num_monstre, décalage + 8))
                        break
                    if num_attr == 17:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 18:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 6))
                        break
                    if num_attr == 19:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 6))
                        break
                    if num_attr == 20:
                        resultsCarac.append((num_monstre, décalage + 0))
                        break
                    if num_attr == 21:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 4))
                        break
                    if num_attr == 22:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 7))
                        break
                    if num_attr == 23:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 6))
                        break
                    if num_attr == 24:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 6))
                        break
                    if num_attr == 25:
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 26:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 7))
                        break
                    if num_attr == 27:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 1))
                        break
                    if num_attr == 28:
                        resultsCarac.append((num_monstre, décalage + 16))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 29:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 30:
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 31:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 1))
                        break
                    if num_attr == 32:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 33:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 34:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 2))
                        break
                    if num_attr == 35:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 36:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 13))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 37:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 38:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 2))
                        break
                    if num_attr == 39:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 5))
                        break
                    if num_attr == 40:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 41:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 4))
                        break
                    if num_attr == 42:
                        resultsCarac.append((num_monstre, décalage + 0))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 3))
                        resultsCarac.append((num_monstre, décalage + 4))
                        resultsCarac.append((num_monstre, décalage + 5))
                        resultsCarac.append((num_monstre, décalage + 6))
                        resultsCarac.append((num_monstre, décalage + 7))
                        resultsCarac.append((num_monstre, décalage + 8))
                        resultsCarac.append((num_monstre, décalage + 13))
                        break
                    if num_attr == 43:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 5))
                        break
                    if num_attr == 44:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 2))
                        break
                    if num_attr == 45:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 7))
                        break
                    if num_attr == 46:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 5))
                        break
                    if num_attr == 47:
                        resultsCarac.append((num_monstre, décalage + 22))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 48:
                        resultsCarac.append((num_monstre, décalage + 16))
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 49:
                        resultsCarac.append((num_monstre, décalage + 20))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 50:
                        resultsCarac.append((num_monstre, décalage + 1))
                        break
                    if num_attr == 51:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 13))
                        resultsCarac.append((num_monstre, décalage + 4))
                        break
                    if num_attr == 52:
                        resultsCarac.append((num_monstre, décalage + 16))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 53:
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 54:
                        resultsCarac.append((num_monstre, décalage + 0))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 3))
                        resultsCarac.append((num_monstre, décalage + 4))
                        resultsCarac.append((num_monstre, décalage + 5))
                        resultsCarac.append((num_monstre, décalage + 6))
                        resultsCarac.append((num_monstre, décalage + 7))
                        resultsCarac.append((num_monstre, décalage + 8))
                        resultsCarac.append((num_monstre, décalage + 12))
                        break
                    if num_attr == 55:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 13))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 3))
                        resultsCarac.append((num_monstre, décalage + 5))
                        resultsCarac.append((num_monstre, décalage + 6))
                        resultsCarac.append((num_monstre, décalage + 7))
                        resultsCarac.append((num_monstre, décalage + 8))
                        break
                    if num_attr == 56:
                        resultsCarac.append((num_monstre, décalage + 24))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 57:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 13))
                        resultsCarac.append((num_monstre, décalage + 8))
                        break
                    if num_attr == 58:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 59:
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 60:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 5))
                        break
                    if num_attr == 61:
                        resultsCarac.append((num_monstre, décalage + 0))
                        resultsCarac.append((num_monstre, décalage + 1))
                        resultsCarac.append((num_monstre, décalage + 2))
                        resultsCarac.append((num_monstre, décalage + 3))
                        resultsCarac.append((num_monstre, décalage + 4))
                        resultsCarac.append((num_monstre, décalage + 5))
                        resultsCarac.append((num_monstre, décalage + 6))
                        resultsCarac.append((num_monstre, décalage + 7))
                        resultsCarac.append((num_monstre, décalage + 8))
                        resultsCarac.append((num_monstre, décalage + 9))
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 12))
                        resultsCarac.append((num_monstre, décalage + 13))
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 15))
                        resultsCarac.append((num_monstre, décalage + 16))
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 18))
                        resultsCarac.append((num_monstre, décalage + 19))
                        resultsCarac.append((num_monstre, décalage + 20))
                        resultsCarac.append((num_monstre, décalage + 21))
                        resultsCarac.append((num_monstre, décalage + 22))
                        resultsCarac.append((num_monstre, décalage + 23))
                        resultsCarac.append((num_monstre, décalage + 24))
                        break
                    if num_attr == 62:
                        resultsCarac.append((num_monstre, décalage + 11))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 63:
                        resultsCarac.append((num_monstre, décalage + 10))
                        resultsCarac.append((num_monstre, décalage + 3))
                        break
                    if num_attr == 64:
                        resultsCarac.append((num_monstre, décalage + 19))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 65:
                        resultsCarac.append((num_monstre, décalage + 2))
                        break
                    if num_attr == 66:
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 67:
                        resultsCarac.append((num_monstre, décalage + 14))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break
                    if num_attr == 68:
                        resultsCarac.append((num_monstre, décalage + 16))
                        resultsCarac.append((num_monstre, décalage + 17))
                        resultsCarac.append((num_monstre, décalage + 9))
                        break

    décalage += len(environnementsToWrite)
    decalages.append(décalage)
    for num_attr, attrname in enumerate(jetsSauvegardes_xml):
        seuil = seuilsJetsSauvegardes[num_attr]
        attr_node = monstre.find('saves/save[@class="' + attrname + '"]')
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                if '*' in val:
                    val, machin = val.split("*")
                if '(' in val:
                    val, machin = val.split("(")
                if '+' in val:
                    machin, val = val.split("+")
                score = 0
                val = int(val)
                if val < seuil:
                    score = 0
                else:
                    score = 1
                resultsCarac.append((num_monstre, décalage + 2 * num_attr + score))

    décalage += len(jetsSauvegardes) * len(classesCaracJetsSauvegardes)
    decalages.append(décalage)
    for num_attr, attrname in enumerate(caracs_xml):
        seuil = seuilsCarac[num_attr]
        attr_node = monstre.find('caracs/carac[@class="' + attrname + '"]')
        if attr_node != None:
            val = attr_node.text.strip()
            if val:
                if '*' in val:
                    val, machin = val.split("*")
                if num_attr == 0:
                    score = 0
                    if '-' == val:
                        score = 0
                    else:
                        val = int(val)
                        if val < seuil[0]:
                            score = 0
                        elif seuil[0] <= val < seuil[1]:
                            score = 1
                        else:
                            score = 2
                    resultsCarac.append((num_monstre, décalage + 3 * num_attr + score))
                if num_attr == 1:
                    score = 0
                    if '-' == val:
                        score = 0
                    else:
                        val = int(val)
                        if val < seuil:
                            score = 0
                        else:
                            score = 1
                    resultsCarac.append((num_monstre, décalage + 3 * num_attr + score))
                if num_attr == 2:
                    score = 0
                    if '-' == val:
                        score = 0
                    else:
                        val = int(val)
                        if val < seuil:
                            score = 1
                        else:
                            score = 2
                    resultsCarac.append((num_monstre, décalage + 2 * num_attr + score + 1))
                if num_attr == 3:
                    score = 0
                    if '-' == val:
                        score = 0
                    else:
                        val = int(val)
                        if val < seuil[0]:
                            score = 1
                        elif seuil[0] <= val < seuil[1]:
                            score = 2
                        else:
                            score = 3
                    resultsCarac.append((num_monstre, décalage + 3 * num_attr + score - 1))
                if num_attr == 4:
                    score = 0
                    if '-' == val:
                        score = 0
                    else:
                        val = int(val)
                        if val < seuil[0]:
                            score = 0
                        elif seuil[0] <= val < seuil[1]:
                            score = 1
                        else:
                            score = 2
                    resultsCarac.append((num_monstre, décalage + 3 * num_attr + score))
                if num_attr == 5:
                    score = 0
                    if '-' == val:
                        score = 0
                    else:
                        val = int(val)
                        if val < seuil[0]:
                            score = 0
                        elif seuil[0] <= val < seuil[1]:
                            score = 1
                        else:
                            score = 2
                    resultsCarac.append((num_monstre, décalage + 3 * num_attr + score))
    decalages.append(décalage + len(caracs))

f = open('galicia.bin.xml', 'w')
f.write('<BIN name="Default Name" nbObj="%d" nbAtt="%d" type="BinaryRelation">\n' % (420, 97))#(num_monstre + 1, decalages[9]))
f.write('<OBJS>\n')
for num_monstre, monstre in enumerate(monstres):
    f.write('<OBJ id="%d">%s</OBJ>\n' % (num_monstre, monstre))
f.write('</OBJS>\n')
f.write('<ATTS>\n')
for num_carac, carac in enumerate(types):
    f.write('<ATT id="%d">%s</ATT>\n' % (num_carac, carac))
for num_carac, carac in enumerate(tailles):
    f.write('<ATT id="%d">%s</ATT>\n' % (decalages[0] + num_carac, carac))
for num_carac, carac in enumerate(facteurs):
    if num_carac == 0:
        for num_classe, classe in enumerate(classesCaracFacteur1):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[1] + 4 * num_carac + num_classe, carac, classe))
    if num_carac == 1:
        for num_classe, classe in enumerate(classesCaracFacteur2):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[1] + 4 * num_carac + num_classe, carac, classe))
    if num_carac == 2:
        for num_classe, classe in enumerate(classesCaracFacteur3):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[1] + 4 * num_carac + num_classe, carac, classe))
            #decalages[2] = decalages[1] + 4 * num_carac + num_classe + 1
for num_carac, carac in enumerate(classeArmure):
    for num_classe, classe in enumerate(classesCaracArmure):
        f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[2] + 4 * num_carac + num_classe, carac, classe))
        #decalages[3] = decalages[2] + 4 * num_carac + num_classe + 1
for num_carac, carac in enumerate(attaqueBase):
    for num_classe, classe in enumerate(classesCaracAttaqueBase):
        f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[3] + 2 * num_carac + num_classe, carac, classe))
        #decalages[4] = decalages[3] + 2 * num_carac + num_classe + 1
for num_carac, carac in enumerate(attaqueLutte):
    for num_classe, classe in enumerate(classesCaracAttaqueLutte):
        f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[4] + 4 * num_carac + num_classe, carac, classe))
        #decalages[5] = decalages[4] + 4 * num_carac + num_classe + 1
for num_carac, carac in enumerate(alignements):
    f.write('<ATT id="%d">%s</ATT>\n' % (decalages[5] + num_carac, carac))
    #decalages[6] = decalages[5] + num_carac + 1
for num_carac, carac in enumerate(environnementsToWrite):
    f.write('<ATT id="%d">%s</ATT>\n' % (decalages[6] + num_carac, carac))
    #decalages[7] = decalages[6] + num_carac + 1
for num_carac, carac in enumerate(jetsSauvegardes):
    for num_classe, classe in enumerate(classesCaracJetsSauvegardes):
        f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[7] + 2 * num_carac + num_classe, carac, classe))
        #decalages[8] = decalages[7] + 2 * num_carac + num_classe + 1

for num_carac, carac in enumerate(caracs):
    if num_carac == 0:
        for num_classe, classe in enumerate(classesCarac1):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[8] + 3 * num_carac + num_classe, carac, classe))
    if num_carac == 1:
        for num_classe, classe in enumerate(classesCarac2):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[8] + 3 * num_carac + num_classe, carac, classe))
    if num_carac == 2:
        for num_classe, classe in enumerate(classesCarac3):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[8] + 2 * num_carac + num_classe + 1, carac, classe))
    if num_carac == 3:
        for num_classe, classe in enumerate(classesCarac4):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[8] + 3 * num_carac + num_classe - 1, carac, classe))
    if num_carac == 4:
        for num_classe, classe in enumerate(classesCarac5):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[8] + 3 * num_carac + num_classe, carac, classe))
    if num_carac == 5:
        for num_classe, classe in enumerate(classesCarac6):
            f.write('<ATT id="%d">%s %s</ATT>\n' % (decalages[8] + 3 * num_carac + num_classe, carac, classe))

f.write('</ATTS>\n')
f.write('<RELS>\n')
for obj, attr in resultsCarac:
    f.write('<REL idObj="%d" idAtt="%d"></REL>\n' % (obj, attr))
f.write('</RELS>\n')
f.write('</BIN>\n')

'''
f = open('galicia.bin.xml', 'w')
f.write('<Galicia_Document>\n')
f.write('<BinaryContext numberObj="%d" numberAtt="%d">\n' % (num_monstre + 1, 3 * len(caracs)))
f.write('<Name> Ctx_0 </Name>\n')
for monstre in monstres:
    f.write('<Object>%s</Object>\n' % monstre)
for carac in caracs:
    for classe in classesCarac:
        f.write('<Attribute>%s %s</Attribute>\n' % (carac, classe))
for obj, attr in resultsCarac:
    f.write('<BinRel idxO="%d" idxA="%d"></BinRel>\n' % (obj, attr))
f.write('</BinaryContext>\n')
f.write('</Galicia_Document>\n')
'''