#!/usr/bin/python
# --*-- coding: latin-1 --*--

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from unidecode import unidecode
import urllib2, sys, io
import xml.etree.ElementTree as ET

##################################
# Parser de l'index Alphabetique #
##################################

class AlphabetHTMLParser(HTMLParser):
    sti = False
    prt = False
    link = ""
    links = []

    # printer
    def to_print(self, n, msg):
        if (msg == 'div'):
            self.prt = False
            self.sti = False
        elif (msg == 'a'):
            if (n == 0):
                self.prt = True
            elif (n == 2):
                self.prt = False
        if (self.prt and self.sti):
            if (n==0):
                if (msg == 'a'):
                    self.link = True
            elif (n==1):
                if (msg[0] == 'href' ):
                    self.link = msg[1]
            elif (n==2):
                if (msg == 'a'):
                    link = False
            elif (n==3 and len(msg) == 1):
                self.links.append(self.link)
        return

    # handlers
    def handle_starttag(self, tag, attrs):
        self.to_print(0, tag)
        if (tag == 'a'):
            self.prt = True
        for attr in attrs:
            if (attr == ('class', 'subtopicitem')):
                self.sti = True
            elif (attr[0] == 'href') :
                self.link = attr[1]
            self.to_print(1, attr)

    def handle_endtag(self, tag):
        self.to_print(2, tag)

    def handle_data(self, data):
        self.to_print(3, data)

    def handle_comment(self, data):
        self.to_print(4, data)

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        self.to_print(5, c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
            self.to_print(6, c)

    def handle_decl(self, data):
        self.to_print(7, data)


##################################
# Parser de l'index d'une lettre #
##################################

class LetterHTMLParser(HTMLParser):
    sti = False
    prt = False
    ble = False
    link = ""
    links = []
    letter = ""

    # printer
    def to_print(self, n, msg):
        if ((msg == ('class', 'subtopicitem')) and n==1):
            self.sti = True
        elif ((msg == ('class', 'topicLineFirst')) and n==1):
            self.ble = True
        elif (msg == 'div'):
            self.prt = False
            self.sti = False
        elif (msg == 'a'):
            if (n == 0):
                self.prt = True
            elif (n == 2):
                self.prt = False
        if (self.prt and self.sti):
            if (n==0):
                if (msg == 'a'):
                    self.link = True
            elif (n==1):
                if (msg[0] == 'href' ):
                    self.link = msg[1]
            elif (n==2):
                if (msg == 'a'):
                    link = False
            elif (n==3 and msg[0] == self.letter):
                self.links.append(self.link)
        if (self.ble and n == 3):
            self.letter = msg
            self.ble = False
        return

    # handlers
    def handle_starttag(self, tag, attrs):
        self.to_print(0, tag)
        for attr in attrs:
            self.to_print(1, attr)

    def handle_endtag(self, tag):
        self.to_print(2, tag)

    def handle_data(self, data):
        self.to_print(3, data)

    def handle_comment(self, data):
        self.to_print(4, data)

    def handle_entityref(self, name):
        #c = unichr(name2codepoint[name])
        self.to_print(5, name)

    def handle_charref(self, name):
        #if name.startswith('x'):
        #    c = unichr(int(name[1:], 16))
        #else:
        #    c = unichr(int(name))
        self.to_print(6, name)

    def handle_decl(self, data):
        self.to_print(7, data)


#####################
# Parser monstrueux #
#####################

class MonsterHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.ttn = False # in TopicTextNotes html class
        self.tbl = False # inside the caract table
        self.div = False # div section
        self.tlf = False # topicLineFirst span section
        self.accu = ""   # accumulator

        self.datas = []

    # handlers
    def handle_starttag(self, tag, attrs):
        if (tag == 'div'):
            self.div = True
        elif (tag == 'table'):
            self.tbl = True
        elif (tag == 'b'):
            self.bld = True
        for attr in attrs:
            if (attr == ('class', 'topicTextNotes')):
                self.ttn = True
            elif (attr == ('class', 'topicLineFirst')):
                self.tlf = True
            elif (attr == ('id', 'pageFooter')):
                self.tbl = False

    def handle_endtag(self, tag):
        if (self.tlf or (tag == 'div' and self.ttn and self.tbl)):
            self.div = False
            self.tlf = False
            self.datas.append(" ".join((self.accu.replace('\n'," ")).split()))
            self.accu = ''
        elif (tag == 'table'):
            self.tbl = False
        elif (tag == 'b'):
            self.bld = False

    def handle_data(self, data):
        if (self.tlf or (self.ttn and self.tbl and self.div)):
            self.accu += data + " "

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        #c = unichr(name2codepoint[name])
        pass

    def handle_charref(self, name):
        #if name.startswith('x'):
        #    c = unichr(int(name[1:], 16))
        #else:
        #    c = unichr(int(name))
        pass

    def handle_decl(self, data):
        pass


def output(monster):
    mstr = ET.Element('monster')

    ### Nom ###
    ET.SubElement(mstr, 'name', text=monster[0])
    ### Type ###
    data = [dat for dat in monster[1].split() if dat.isalpha()]
    for dat in data[0:len(data)-3]:
        ET.SubElement(mstr, 'type', text=dat)
    ### Taille ###
    ET.SubElement(mstr, 'taille', text=data.pop())
    ### Dés de vie ###
    ET.SubElement(mstr, 'dv', text=monster[2].split(":")[1])
    ### Initiative ###
    ET.SubElement(mstr, 'init', text=monster[3].split(":")[1])
    ### Déplacement ###
    depl = ET.SubElement(mstr, 'depl')
    data = [dat for dat in (monster[4].split(':')[1]).split(",")]
    for dat in data:
        prov = dat.split()
        if prov[0].isalpha():
            ET.SubElement(depl, prov[0], text=prov[1])
        else:
            ET.SubElement(depl, 'marche', text=prov[0])
    ### Classe d'Armure ###
    ca = ET.SubElement(mstr, 'ca')
    data = monster[5].split(":")[1].split("(")[1].split(")")[0].split()
    for i in range(len(data)/2):
        if data[2*i][0].isdigit():
            ET.SubElement(ca, 'bonus', 
                          attrib={'class':data[2*i+1].replace(',','')}, 
                          text=("-" + data[2*i]))
        else:
            ET.SubElement(ca, 'bonus',
                          attrib={'class':data[2*i+1].replace(',','')},
                          text=data[2*i])
    ### Bonus de Base à l'Attaque ###
    bba = ET.SubElement(mstr, 'bba')
    data = monster[6].split(": ")[1].split("/")
    ET.SubElement(bba, 'base', text=data[0])
    ET.SubElement(bba, 'lutte', text=data[1])
    ### Attaques ###
    data = monster[7].split(": ")[1].split("; ou")
    for atqs in data:
        atqs = ET.SubElement(mstr, 'atqs')
        for atq in atqs.split("),"):
            prov = atq.split(" (")
            ET.SubElement(atqs, 'atq', attrib={'name':prov[0]})
            prov2 = prov[1].split(")")[0].split(",")
            ET.SubElement(atq, 'touch', text=prov2[0])
            prov3 = prov2[1].split(" et ")
            ET.SubElementout(atq, 'dgts', text=prov3[0])
            if len(prov3) > 1:
                ET.SubElement(atq, 'effect', text=prov3[1])

    # Attaque à outtrance mise de côté : monster[8]
    # Espace occupé/allonge mise de côté : monster[9]

    ### Attaques Spéciales ###
    data = monster[10].split(":")[1].split(",")
    for skill in data:
        ET.SubElement(mstr, 'skill', text=skill)
    ### Particularités ###
    data = monster[11].split(": ")[1].split(',')
    for feat in data:
        ET.SubElement(mstr, 'quality', text=feat)
    ### Sauvegardes ###
    data = monster[12].split(": ")[1].split(',')
    saves = ET.SubElement(mstr, 'saves')
    for save in data:
        prov = save.split('\xc2\xa0')
        ET.SubElement(saves, 'save', 
                      attrib={'class':prov[0].replace(' ','')},
                      text=prov[1])
    ### Caractéristiques ###
    data = monster[13].split(": ")[1].split(',')
    caracs = ET.SubElement(mstr, 'caracs')
    for carac in data:
        prov = carac.split('\xc2\xa0')
        if not prov[0]:
            prov.pop(0)

        ET.SubElement(caracs, 'carac',
                      attrib={'class':prov[0].replace(' ','')},
                      text=prov[1])
    ### Compétences ###
    data = monster[14].split(": ")[1].split(',')
    comps = ET.SubElement(mstr, 'comps')
    for comp in data:
        prov = comp.split(" +")
        ET.SubElement(comps, 'comp',
                      attrib={'class':prov[0].replace(' ','').replace(' ','')[0:7]},
                      text=prov[1])
    ### Dons ###
    data = monster[15].split(": ")[1].split(',')
    for feat in data:
        ET.SubElement(mstr, 'feat', text=feat)
    ### Environnement ###
    data = monster[16].split(": ")[1].split(',')
    for env in data:
        ET.SubElement(mstr, 'environ', text=env)
    ### Orga Sociale : on verra après ### : monster[17]
    ### Facteur de Puissance ###
    ET.SubElement(mstr, 'puiss', text=monster[18].split(": ")[1])
    ### Trésors ### on verra après : monster[19]
    ### Alignement ###
    data = monster[20].split(": ")[1]
    bom = ['bon','mauvais','neutre','loyal','chaotique']
    for sub in bom:
        if data.count(sub) > 0:
            ET.SubElement(mstr,'align', text=sub)
    ### Évolutions possible ### on verra... ou pas
    ### Ajustement de niveau ### ou pas!

    return ET.tostring(mstr)


######################
#  Script de Parsing #
######################

if len(sys.argv) < 2:
    print "Please, output file path is necessary!"
else:

    base_url = "http://www.regles-donjons-dragons.com/"

    ### Get the monsters ###

    monsters_url = "Page1676.html"

    parser = AlphabetHTMLParser()

    response = urllib2.urlopen(base_url + monsters_url)
    page_source = response.read()

    parser.feed(page_source)

    alphabet = parser.links

    ### Get the monsters links ###
    for letterLink in alphabet :

        parser = LetterHTMLParser()

        response = urllib2.urlopen(base_url + letterLink)
        page_source = response.read()

        parser.feed(page_source)

    monsters = parser.links
    print len(monsters)

    i = 0
    ### Get monsters caracs ###
    monsters.reverse()
    with io.open(sys.argv[1], 'wb') as my_file:
        for monster_url in monsters:

            parser = MonsterHTMLParser()

            response = urllib2.urlopen(base_url + monster_url)
            page_source = response.read()

            parser.feed(page_source)

            out = ''
            try:
                out = output(parser.datas)
                my_file.write(out)
                i = i + 1
            except:
                pass

    print i
