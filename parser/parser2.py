#!/usr/bin/python
# --*-- coding: latin-1 --*--

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from unidecode import unidecode
from xml.dom import minidom
import urllib2, sys, io
import xml.etree.ElementTree as ET


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

#####################
#   Listing Parser  #
#####################

class ListingHTMLParser(HTMLParser):

  def __init__(self):
    HTMLParser.__init__(self)
    self.creas = False    # in d20 dragon monstats class table
    self.accu = ""        # accumulator

    self.datas = []

  # handlers
  def handle_starttag(self, tag, attrs):
    for attr in attrs:
      if (attr == ('id', 'Creatures')):
        self.creas = True
      elif (self.creas and attr[0] == 'href'):
        self.datas.append(attr[1])

  def handle_endtag(self, tag):
    if (tag == 'table'):
      self.creas = False

  def handle_data(self, data):
    pass

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


#####################
# Parser monstrueux #
#####################

class MonsterHTMLParser(HTMLParser):

  def __init__(self):
    HTMLParser.__init__(self)
    self.stats = False    # in d20 dragon monstats class table
    self.headtag = False  # inside table header
    self.datatag = False  # inside table data
    self.ignore  = False  # erratums � ignorer
    self.name = False     # mon-stats table section
    self.accu = ""        # accumulator

    self.datas = []

  # handlers
  def handle_starttag(self, tag, attrs):
    if (self.stats):
      if (tag == 'th'):
        self.headtag = True
      elif (tag == 'td'):
        self.datatag = True
      elif (tag == 's'):
        self.ignore = True
    for attr in attrs:
      if (attr == ('class', 'd20 dragon monstats')):
        self.stats = True
      elif (attr == ('class', 'mw-headline')):
        self.name = True

  def handle_endtag(self, tag):
    if (tag == 'table'):
      self.stats = False
    elif (tag == 'th'):
      if (self.stats and (self.accu not in ['',' ']) and (len(self.datas) < 1)):
        self.datas.append(" ".join((self.accu.replace('\n'," ")).split()))
      self.accu = ''
      self.headtag = False
    elif (tag == 'td'):
      if (self.stats and self.datatag) :
        self.datas.append(" ".join((self.accu.replace('\n'," ")).split()))
        self.accu = ''
      self.datatag = False
    elif (tag == 's'):
      self.ignore = False
    elif (self.name) :
      self.datas.append(" ".join((self.accu.replace('\n'," ")).split()))
      self.accu = ''
      self.name = False

  def handle_data(self, data):
    if ((self.stats and self.datatag and not self.ignore) or self.name or self.headtag) :
      self.accu += data.translate(None, '\n')

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

def prettify(elem):
  """Return a pretty-printed XML string"""
  rough_string = ET.tostring(elem)
  reparsed = minidom.parseString(rough_string)
  return reparsed.toprettyxml(indent="  ")

def output(monster):
  mstr = ET.Element('monster')

  print monster[0]
  ### Nom ###
  elem = ET.SubElement(mstr, 'name')
  elem.text = monster[0].replace('\xe2\x80\x99','\'')
  ### Type ###
  data = [dat for dat in monster[1].split() if dat.isalpha()]
  for dat in data[1:]:
    elem = ET.SubElement(mstr, 'type')
    elem.text = dat
  ### Taille ###
  elem = ET.SubElement(mstr, 'taille')
  elem.text = data[0]
  ### Dés de vie ###
  elem = ET.SubElement(mstr, 'dv')
  elem.text = monster[2].replace('\xe2\x80\x93','-')
  ### Initiative ###
  elem = ET.SubElement(mstr, 'init')
  elem.text = monster[3].replace('\xe2\x80\x93','-')
  ### Déplacement ###
  depl = ET.SubElement(mstr, 'depl')
  data = [dat for dat in monster[4].split(",")]
  for dat in data:
    prov = dat.split()
    if prov[0].isalpha():
      elem = ET.SubElement(depl, prov[0])
      elem.text = prov[1].replace('\xe2\x80\x99','\'')
    else:
      elem = ET.SubElement(depl, 'marche')
      elem.text = prov[0].replace('\xe2\x80\x99','\'')
  ### Classe d'Armure ###
  ca = ET.SubElement(mstr, 'ca')
  data = monster[5].replace('–','-').split("(")[1].split(")")[0].split(',')
  for bon in data:
    b = bon.split()
    elem = ET.SubElement(ca, 'bonus',
        attrib={'class':b[1]})
    elem.text=b[0].replace('\xe2\x80\x93','-')
  ### Bonus de Base à l'Attaque ###
  bba = ET.SubElement(mstr, 'bba')
  data = monster[6].split("/")
  elem = ET.SubElement(bba, 'base')
  elem.text = data[0].replace('\xe2\x80\x93','-')
  if not (data[1] == '\xe2\x80\x94'):
    elem = ET.SubElement(bba, 'lutte')
    elem.text = data[1].replace('\xe2\x80\x93','-')
  ### Attaques ###
  data = monster[7].split(" or ")
  for atqs in data:
    atqs_el = ET.SubElement(mstr, 'atqs')
    for atq in atqs.split(","):
      prov = atq.translate(None, '()').split(" ")
      atq_el = ET.SubElement(atqs_el, 'atq', attrib={'name':prov[0]})
      elem = ET.SubElement(atq_el, 'touch')
      elem.text = prov[1].replace('\xe2\x80\x93','-')
      elem = ET.SubElement(atq_el, 'type' )
      elem.text = prov[2]
      elem = ET.SubElement(atq_el, 'dgts' )
      elem.text = prov[3].replace('\xe2\x80\x93','-')
      # Effects pas pris en compte pour le moment
      #if len(prov3) > 1:
      #  ET.SubElement(atq, 'effect', text=prov3[1])

  ## Attaque à outtrance mise de côté : monster[8]
  ## Espace occupé/allonge mise de côté : monster[9]

  ### Attaques Spéciales ###
  if (monster[10] != '\xe2\x80\x94'):
    data = monster[10].split(",")
    for skill in data:
      elem = ET.SubElement(mstr, 'skill')
      elem.text = skill.replace('\xe2\x80\x93','-')
  ### Particularités ###
  if (monster[11] != '\xe2\x80\x94'):
    data = monster[11].split(',')
    for feat in data:
      elem = ET.SubElement(mstr, 'quality')
      elem.text = feat.replace('\xe2\x80\x99','\'').replace('\xe2\x80\x93','-')
  ### Sauvegardes ###
  data = monster[12].split(',')
  saves = ET.SubElement(mstr, 'saves')
  for save in data:
    prov = save.split()
    elem = ET.SubElement(saves, 'save',
        attrib={'class':prov[0].translate(None, ' ')})
    elem.text = prov[1].replace('\xe2\x80\x93','-')
  ### Caractéristiques ###
  data = monster[13].split(',')
  caracs = ET.SubElement(mstr, 'caracs')
  for carac in data:
    prov = carac.split()
    if not prov[0]:
      prov.pop(0)
    elem = ET.SubElement(caracs, 'carac',
        attrib={'class':prov[0]})
    elem.text = prov[1].replace('\xe2\x80\x94','-').replace('\xe2\x80\x93','-')
  ### Compétences ###
  if (monster[14] != '\xe2\x80\x94'):
    data = monster[14].split(',')
    comps = ET.SubElement(mstr, 'comps')
    for comp in data:
      prov = comp.split()
      elem = ET.SubElement(comps, 'comp',
          attrib={'class':prov[0]})
      elem.text = prov[1].replace('\xe2\x80\x94','-').replace('\xe2\x80\x93','-')
  ### Dons ###
  if (monster[15] != '\xe2\x80\x94'):
    data = monster[15].split(',')
    for feat in data:
      elem = ET.SubElement(mstr, 'feat')
      elem.text = feat
  ### Environnement ###
  data = monster[16].split(',')
  for env in data:
    elem = ET.SubElement(mstr, 'environ')
    elem.text = env
  ### Orga Sociale : on verra après ### : monster[17]
  ### Facteur de Puissance ###
  elem = ET.SubElement(mstr, 'puiss')
  elem.text = monster[18]
  ### Trésors ### on verra après : monster[19]
  ### Alignement ###
  data = monster[20]
  bom = ['good','evil','neutral','loyal','chaotic']
  for sub in bom:
    if data.count(sub) > 0:
      elem = ET.SubElement(mstr,'align')
      elem.text = sub
  ### Évolutions possible ### on verra... ou pas
  ### Ajustement de niveau ### ou pas!

  return mstr


######################
#  Script de Parsing #
######################

if len(sys.argv) < 2:
  print "Please, output file path is necessary!"
else:

  base_url = "http://www.dandwiki.com"
  list_url = "/wiki/SRD:Creatures"
  #monster_expl_url = "/wiki/SRD:Medium_Animated_Object"

  ### Get the monsters ###

  parser = ListingHTMLParser()

  req = urllib2.Request(base_url + list_url, headers = hdr)

  response = urllib2.urlopen(req)
  page_source = response.read()

  parser.feed(page_source)

  monsters = parser.datas
  print len(monsters), 'monsters to parse'

  exceptions = ['/wiki/SRD:Elder_Treant','/wiki/SRD:Hunefer','/wiki/SRD:Sirrush','/wiki/SRD:Three-Headed_Sirrush','/wiki/SRD:Vermiurge','/wiki/SRD:Winterwight']
  for e in exceptions:
    monsters.remove(e)
  out = ET.Element('monsters')
  i = 0

  with io.open(sys.argv[1], 'wb') as my_file:
    for monster_url in monsters:
      parser = MonsterHTMLParser()

      req = urllib2.Request(base_url + monster_url, headers = hdr)

      response = urllib2.urlopen(req)
      page_source = response.read()

      parser.feed(page_source)

      try:
        mstr = output(parser.datas)
        out.append(mstr)
        i = i+1
      except:
        print monster_url, 'not counted in'
        print sys.exc_info()
        print sys.exec_prefix
        pass
      
    my_file.write(prettify(out))
      

  print i, 'monsters totally counted'


