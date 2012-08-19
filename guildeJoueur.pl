use WWW::Mechanize;
# use Digest::SHA1;
use strict;
use warnings;


my $ua="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1";
my $login="etiandre";
my $password="louloul";



my $joueur=shift; # joueur récupéré dans les arguments du script
if ($joueur eq $login) { # sinon ça fait des erreurs vu que la page est différente
    print "Rien d'intéressant ici, petit curieux!\n";
    exit();
}

my $mech = WWW::Mechanize->new();
$mech->agent($ua);
$mech->get("http://www.nemeria.com/auth");
$mech->submit_form(
	form_number => 1,
	fields => {
		username=>$login,
		password=>"",
        sha1password=>"334b3b6db54ec9126b12e29fcaa972b7e138c6a3",
        remember=>0
	}
);
$mech->get("http://aurora.nemeria.com/suggestion/searchJoueur?term=$joueur");
if ($mech->content() eq "[]") {
    print("Pas de résultat de recherche pour $joueur.\n");
    exit();
}
my $id;
if ($mech->content() =~ /\[\{"id":(\d+),"nom":"($joueur)"/i) {
    $id=$1;
    $joueur=$2;
}
$mech->get("http://aurora.nemeria.com/profil?id=$id");
if ($mech->text() =~ /Alliance : (.+)\s+Peuple : (\w+)\s+Population : (\d+)\s+Description.+Classement G\wn\wral : (\d+)/) {
    print "$joueur est un $2 dans l'alliance $1. (pop: $3, classé n°$4) http://aurora.nemeria.com/profil?id=$id\n";
} else {
    print "Erreur lors de la récupération des infos pour $joueur.\n";
    print STDERR $mech->text();
}
