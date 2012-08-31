use strict;
use warnings;
use LWP::Simple;
use Data::Dumper;
use XML::Simple;
use DBI;

$|=1;
my $monde=shift or die("Usage: $0 <bellios|aurora>\n");
my $db = DBI->connect("dbi:SQLite:dbname=$monde.db");
my $r;
$db->do('DROP TABLE IF EXISTS joueurs');
$db->do('DROP TABLE IF EXISTS alliances');
$db->do('DROP TABLE IF EXISTS villes');
$db->do('CREATE TABLE "alliances" (
  "id" integer NOT NULL,
  "nom" varchar(20) NOT NULL,
  "pop" integer NOT NULL,
  "classement" integer NOT NULL
)');
$db->do('CREATE TABLE "joueurs" (
  "id" integer NOT NULL,
  "nom" varchar(20) NOT NULL,
  "pop" integer NOT NULL,
  "classement" integer NOT NULL,
  "id_alliance" integer NOT NULL,
  PRIMARY KEY ("id")
)');
$db->do('CREATE TABLE "villes" (
  "id" integer NOT NULL,
  "terrain" integer NOT NULL,
  "id_joueur" integer NOT NULL,
  "nom" varchar(20) NOT NULL,
  "pop" integer NOT NULL
)');
#~ my $content=get("http://$monde.nemeria.com/ext");
open(my $f,"$monde.xml");
my $content=<$f>;
close($f);
my $ref=XMLin($content, ForceArray=>['joueur']);
my $joueurs=$ref->{'joueurs'}->{'joueur'};
my $alliances=$ref->{'alliances'}->{'alliance'};
my $villes=$ref->{'villes'}->{'ville'};
$r=$db->prepare("INSERT into villes (id,terrain,id_joueur,nom,pop) VALUES (?,?,?,?,?);");
print(keys($villes)." villes, ");
foreach my $v (keys $villes) {
    print STDERR ".";
    $r->execute(
        $v,
        $villes->{$v}->{'terrain'},
        $villes->{$v}->{'joueur'}[0],
        $villes->{$v}->{'nom'},
        $villes->{$v}->{'population'},
    ) or print($v.Dumper($villes->{$v}));
}

$r=$db->prepare("INSERT into alliances (id,nom,pop,classement) VALUES (?,?,?,?);");
print(keys($alliances)." alliances, ");
foreach my $a (keys $alliances) {
    print STDERR ".";
    $r->execute(
        $a,
        $alliances->{$a}->{'nom'},
        $alliances->{$a}->{'population'},
        $alliances->{$a}->{'classement'},
    ) or print($a.Dumper($alliances->{$a}));
}

print(keys($joueurs)." joueurs.\n");
$r=$db->prepare("INSERT into joueurs (id,nom,pop,classement,id_alliance) VALUES (?,?,?,?,?);");
foreach my $j (keys $joueurs) {
    print STDERR ".";
    my $alli=$joueurs->{$j}->{'alliance'}->{'id'};
    $alli=-1 unless ($alli);
    $r->execute(
        $j,
        $joueurs->{$j}->{'nom'},
        $joueurs->{$j}->{'population'},
        $joueurs->{$j}->{'classement'},
        $alli
    );
}


