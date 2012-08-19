#!/usr/bin/env python2
# -*- coding: utf8 -*-

import os
import ircbot
import irclib
import random
import re
import pickle
import commands

class Bot(ircbot.SingleServerIRCBot):
    def __init__(self):
        print "Connexion en cours..."
        ircbot.SingleServerIRCBot.__init__(self, [("irc.nemeria.com", 6667)],
                                           "NemeBot", "NemeBot")
        self.chan="#nemeria" # modifier ici le chan où se connecter
    def on_welcome(self, serv, ev):
        serv.join(self.chan)
        print "Réussi"
        serv.privmsg(self.chan, "NemeBot par eti.andre@gmail.com est sur "+self.chan+". !help pour une liste des commandes.")
    def on_pubmsg(self, serv, ev):
        message = ev.arguments()[0]
        pseudo=ev.source().split("!")[0].lower()
        if pseudo=="etiandre":
            if message=="!quit":
                print "deco"
                serv.disconnect("Bye")
                exit()
        # partie pour interfacer avec le bot "Dieu" de Twan, à supprimer si non nécessaire
        if not "nemebot" in message and "on applaudit" in message.lower() and "dieu" in pseudo:
             serv.privmsg(self.chan,"clap clap")
        if "ça va" in message.lower() and "nemebot" in message.lower() and "dieu" in pseudo:
            serv.privmsg(self.chan,"Tranquille wesh, et toi Dieu?")
        # fin de l'interfacage avec Dieu
        if message.startswith("!joueur"):
            try:
                arg=message.split("!joueur ")[1]
                if arg=="" or re.search(r"[^\w\s]",arg):
                    raise ValueError
            except:
                serv.privmsg(self.chan, "Usage: !joueur <joueur>")
            else:
                print "recherche d'infos sur", arg
                serv.privmsg(self.chan,commands.getoutput("/usr/bin/perl joueur.pl " + arg))
                print "terminé"
        elif message.startswith("!ville"):
            try:
                arg=message.split("!ville ")[1]
                if arg=="" or re.search(r"[^\w\s]",arg):
                    raise ValueError
            except:
                serv.privmsg(self.chan, "Usage: !ville <ville>")
            else:
                print "recherche ville", arg
                serv.privmsg(self.chan,commands.getoutput("/usr/bin/perl ville.pl '" + arg + "'",))
                print "terminé"
        elif message.startswith("!alliance"):
            try:
                arg=message.split("!alliance ")[1]
                if arg=="" or re.search(r"[^\w\s]",arg):
                    raise ValueError
            except:
                serv.privmsg(self.chan, "Usage: !alliance <alliance>")
            else:
                print "recherche alliance", arg
                serv.privmsg(self.chan,commands.getoutput("/usr/bin/perl guilde.pl '" + arg + "'"))
                print "terminé"
        elif message.startswith("!help"):
            serv.privmsg(self.chan,"Commandes dispo pour NemeBot: !joueur !ville !alliance.")
    def on_join(self, serv, ev):
        pseudo = ev.source().split("!")[0].lower()
        if pseudo=="nemebot":
            return
        print pseudo," joined"
        print "recherche d'infos sur", pseudo
        serv.privmsg(self.chan,commands.getoutput("/usr/bin/perl joueur.pl " + pseudo))
        print "terminé"
        if self.chan=="#twan" and ("etiandre" in pseudo or "twan" in pseudo):
            print "Opping "+pseudo
            serv.mode(self.chan," +o " + pseudo)
        elif "alucards" in pseudo: # spécial pour alucards qui appelait NemeBot "boulet" à ses débuts ;P à supprimer si non nécessaire
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
