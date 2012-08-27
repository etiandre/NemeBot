use WWW::Mechanize;

use strict;
use warnings;
use POSIX;


my $ua="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1";
my $login="etiandre";

my $password;
open(my $f, "password") or die("SHA1 du mot de passe à mettre dans le fichier 'password'");
$password=<$f>;
chomp($password);
close($f);

my $ville=shift; # joueur récupéré dans les arguments du script

if ($ville eq "Ealenilir") { # Utiliser ici le nom de la ville du bot. Sinon ça fait des erreurs quand on va chercher les infos, vu que la page a changé.
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
        sha1password=>$password,
        remember=>0
	}
);
$mech->get("http://aurora.nemeria.com/suggestion/searchTerritoire?term=$ville");
if ($mech->content() eq "[]") {
    print("Pas de résultat de recherche pour $ville.\n");
    exit();
}
my $case;
if ($mech->content() =~ /\[\{"id":(\d+),"nom":"($ville)",.+,"nomJoueur":"(\w+)","x":([\d-]+),"y":([\d-]+)/i) {
    $case=(floor(201/2)+$5)*201 + (floor(201/2)+$4); # trouvé dans carte.js .
    # my $x=$case%201 - ceil(201/2-1);
    # my $y=floor($case/201)+1 - ceil(201/2);
    print "$2 de $3 (x=$4,y=$5) http://aurora.nemeria.com/carte?case=$case\n";
} else { print "Erreur lors de la récupération des infos pour $ville.\n"; }
