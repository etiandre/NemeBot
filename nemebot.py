#!/usr/bin/env python2
# -*- coding: utf8 -*-

import os
import ircbot
import irclib
import random
import re
import pickle
import time
import sqlite3

class Bot(ircbot.SingleServerIRCBot):
    def __init__(self):
        print "Connexion en cours..."
        ircbot.SingleServerIRCBot.__init__(self, [("irc.nemeria.com", 6667)],
                                           "SQLNemebot", "SQLNemebot")
        self.chan="#test" # modifier ici le chan où se connecter
        self.sql=sqlite3.connect("nemeria.db").cursor()
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
        if message.startswith("!joueur"):
            try:
                arg=message.split("!joueur ")[1].lower()
                if arg=="" or re.search(r"[^\w\s]",arg):
                    raise ValueError
            except:
                serv.notice(pseudo, "Usage: !joueur <nomdujoueur>")
            else:
                #~ try:
                    self.sql.execute('SELECT * FROM joueurs WHERE nom LIKE ?',(arg,))
                    j=self.sql.fetchone()
                    self.sql.execute('SELECT * FROM alliances WHERE id=?',(j[4],))
                    a=self.sql.fetchone()
                    if a==None: a=(None,"pas d'alliance")
                    serv.privmsg(self.chan, str(j[1])+" ("+str(a[1])+") a "+str(j[2])+" de population et est classé n°"+str(j[3])+". http://aurora.nemeria.com/profil?id="+str(j[0]))
                    s="Villes: "
                    for v in self.sql.execute('SELECT * FROM villes WHERE id_joueur=?',(j[0],)):
                        s+=str(v[3])+"; "
                    serv.privmsg(self.chan, s)
                #~ except:
                    #~ serv.privmsg(self.chan, "Pas trouvé")
        elif message.startswith("!alliance"):
            try:
                arg=message.split("!alliance ")[1]
                if arg=="" or re.search(r"[^\w\s-]",arg):
                    raise ValueError
            except:
                serv.notice(pseudo, "Usage: !alliance <nomdelalliance>")
            else:
                try:
                    self.sql.execute('SELECT * FROM alliances WHERE nom LIKE ?',(arg,))
                    a=self.sql.fetchone()
                    serv.privmsg(self.chan,"Alliance "+str(a[1])+": "+str(a[2])+" de population, classée n°"+str(a[3])+". http://aurora.nemeria.com/alliance?id="+str(a[0]))
                    s="Joueurs: "
                    for j in self.sql.execute('SELECT nom FROM joueurs WHERE id_alliance=?',(a[0],)):
                        s+=str(j[0])+"; "
                    serv.privmsg(self.chan,s)  
                except:
                    serv.privmsg(self.chan,"Pas trouvé.")
        elif message.startswith("!ville"):
            try:
                arg=message.split("!ville ")[1]
                if arg=="" or re.search(r"[^\w\s-]",arg):
                    raise ValueError
            except:
                serv.notice(pseudo, "Usage: !ville <nomdelaville>")
            else:
                try:
                    self.sql.execute('SELECT * FROM villes WHERE nom LIKE ?',(arg,))
                    v=self.sql.fetchone()
                    self.sql.execute('SELECT * FROM joueurs WHERE id=?',(str(v[2]),))
                    j=self.sql.fetchone()
                    serv.privmsg(self.chan,str(v[3])+" ("+j[1]+") a "+str(v[4])+" de population. http://aurora.nemeria.com/carte?case="+str(v[0]))
                except:
                    serv.privmsg(self.chan,"Pas trouvé.")

        elif message.startswith("!help"):
            serv.notice(pseudo,"Commandes dispo pour NemeBot: !joueur !alliance !coords.")
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
