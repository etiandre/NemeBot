use WWW::Mechanize;
use strict;
use warnings;


my $ua="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1";
my $login="etiandre";

my $password;
open(my $f, "password") or die("SHA1 du mot de passe à mettre dans le fichier 'password'");
$password=<$f>;
chomp($password);
close($f);

my $guilde=shift; # joueur récupéré dans les arguments du script

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
$mech->get("http://aurora.nemeria.com/suggestion/searchAlliance?term=$guilde");
if ($mech->content() eq "[]") {
    print("Pas de résultat de recherche pour $guilde.\n");
    exit();
}
my $id;
if ($mech->content() =~ /\[\{"id":(\d+),"nom":"($guilde)"/i) {
    $id=$1;
    $guilde=$2;
}
$mech->get("http://aurora.nemeria.com/alliance?id=$id");


if ($mech->text() =~ /(\d+) joueurs(\d+) habitants.+(\d+) Diplomatie\s+En guerre : (.*) Neutres : (.*) Alli.s :\s+(.*?)\s+Ealenilir/) {
    print "Alliance $guilde: classé n°$3, $1 joueurs avec $2 hab. (Guerre|Neutre|Allié): ($4|$5|$6) http://aurora.nemeria.com/alliance?id=$id\n";
} else {
    print "Erreur lors de la récupération des infos pour $guilde.\n";
    print STDERR $mech->text();
}
