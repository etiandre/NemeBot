NemeBot, un bot irc pour #nemeria fait avec amour par eti.andre@gmail.com

PREREQUIS:

NemeBot est écrit en python2 avec la librairie irclib, à installer.
Les parties qui vont chercher les infos sur Nemeria sont écrites en perl, avec la librairie WWW::Mechanize.

CONFIGURATION:
Dans nemebot.py:
    Editer lignes 15 à 17 l'info du serveur et le chan.
    Supprimer lignes 30 à 35 si on veut pas causer un peu avec "Dieu", le bot de Twan.
    Supprimer lignes 79 à 88 si on veut pas appeler Alucards un boulet :D
Dans guildeJoueur.pl:
    Editer l'user-agent du Bot. ($ua)
    Editer le login du compte utilisé par le bot. ($login)
    Editer le mot de passe de ce compte. ($password)
Dans ville.pl:
    Idem.
Dans extractRapport.pl:
    Idem.

LANCEMENT:
    Lancer nemebot.py avec python2.
    
    

