#!/usr/bin/env python2
# -*- coding: utf8 -*-

import os
import ircbot
import irclib
import random
import re
import pickle
import time
import xml.etree.ElementTree as ET
import urllib

class Bot(ircbot.SingleServerIRCBot):
    def __init__(self):
        print "Connexion en cours..."
        ircbot.SingleServerIRCBot.__init__(self, [("irc.nemeria.com", 6667)],
                                           "NemeBotNG", "NemeBotXML")
        self.chan="#nemeria" # modifier ici le chan où se connecter
        self.updatemonde()
    def updatemonde(self):
        f=open("monde.xml", "w")
        f.write(urllib.urlopen("http://aurora.nemeria.com/ext").read().lower())
        f.close()
        self.xml=ET.parse("monde.xml").getroot()
    def on_welcome(self, serv, ev):
        serv.join(self.chan)
        print "Réussi"
#        serv.privmsg(self.chan, "NemeBot par eti.andre@gmail.com est sur "+self.chan+". !help pour une liste des commandes.")
    def on_pubmsg(self, serv, ev):
        message = ev.arguments()[0]
        pseudo=ev.source().split("!")[0].lower()
        if pseudo=="etiandre":
            if message=="!quit":
                print "deco"
                serv.disconnect("Bye")
                exit()
        if message=="!reload":
            self.updatemonde()
            serv.privmsg(self.chan,"Informations fraîches!")
        if message.startswith("!joueur"):
            try:
                arg=message.split("!joueur ")[1].lower()
                if arg=="" or re.search(r"[^\w\s]",arg):
                    raise ValueError
            except:
                serv.notice(pseudo, "Usage: !joueur <joueur>")
            else:
                try:
                    text=self.xml.find("./joueurs/joueur[nom='"+arg+"']/nom").text
                    try:
                        text+=" ("+self.xml.find('./alliances/alliance[@id="'+(self.xml.find("./joueurs/joueur[nom='"+arg+"']/alliance").attrib['id'])+'"]/nom').text+")"
                    except:
                        pass
                    text+=" population: "+self.xml.find("./joueurs/joueur[nom='"+arg+"']/population").text
                    text+=", classé n°"+self.xml.find("./joueurs/joueur[nom='"+arg+"']/classement").text
                    text+=" http://aurora.nemeria.com/profil?id="+self.xml.find("./joueurs/joueur[nom='"+arg+"']").attrib['id']
                    serv.privmsg(self.chan,text)
                except:
                    serv.privmsg(self.chan,"Pas trouvé.")
        elif message.startswith("!alliance"):
            try:
                arg=message.split("!alliance ")[1]
                if arg=="" or re.search(r"[^\w\s]",arg):
                    raise ValueError
            except:
                serv.notice(pseudo, "Usage: !alliance <alliance>")
            else:
                try:
                    text=self.xml.find("./alliances/alliance[nom='"+arg+"']/nom").text
                    text+=" population: "+self.xml.find("./alliances/alliance[nom='"+arg+"']/population").text
                    text+=", classé n°"+self.xml.find("./alliances/alliance[nom='"+arg+"']/classement").text
                    text+=" http://aurora.nemeria.com/alliance?id="+ self.xml.find("./alliances/alliance[nom='"+arg+"']").attrib['id']
                    serv.privmsg(self.chan,text)           
                except:
                    serv.privmsg(self.chan,"Pas trouvé.")
        elif message.startswith("!coords"):
            try:
                arg=message.split("!coords ")[1]
                x=int(arg.split(" ")[0])
                y=int(arg.split(" ")[1])
                if arg=="" or re.search(r"[^\w\s-]",arg):
                    raise ValueError
            except:
                serv.notice(pseudo, "Usage: !coords <x> <y>")
            else:
                serv.privmsg(self.chan,"http://aurora.nemeria.com/carte?case="+(int(201/2)+y)*201 + (int(201/2)+x))
        elif message.startswith("!help"):
            serv.notice(pseudo,"Commandes dispo pour NemeBot: !joueur !alliance.")
    def on_join(self, serv, ev):
        pseudo = ev.source().split("!")[0].lower()
        if pseudo=="nemebot":
            return
        elif "alucards" in pseudo: # spécial pour alucards qui appelait NemeBot "boulet" à ses débuts ;P
            bouletver=0
            try:
                bouletver=pickle.load(open("bouletver.pickle","rb"))
            except:
                pickle.dump(bouletver,open("bouletver.pickle","wb"))
            bouletver += 1
            print "coucou boulet0.0." + str(bouletver)
            serv.privmsg(self.chan,"coucou boulet0.0." + str(bouletver))
            pickle.dump(bouletver,open("bouletver.pickle","wb"))
if __name__ == "__main__":
    print "Lancement..."
    Bot().start()
