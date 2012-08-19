use WWW::Mechanize;
# use Digest::SHA1;
use strict;
use warnings;



my $ua="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1";
my $login="etiandre";



my $id=shift; # id du rapport récupéré dans les arguments du script
my @unitnames=("Hallebardier","Massier     ","Javelier    ","Berzerk     ","Hussard     ","Cuirassier  ","Baliste     ","Trébuchet   ");
my @resnames=qw(Bois Pierre Fer Vivres Or);
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
$mech->get("http://aurora.nemeria.com/rapport/pub?id=".$id);
my $html=$mech->content();
my $text=$mech->text();
my $date;
if ($text =~ /(\d+\/\d+\/\d+) (\d+:\d+:\d+)/) {
    $date = $1." à ".$2;
}
my $attaquants;
my @units;
if ($text =~ /Attaquant  ([\?A-Za-z\s]+) ([\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+)/) {
    $attaquants=${1};
    @units=split(" ",${2});
    
}
my $defenseurs;
if ($text =~ /D\wfenseur  ([\?A-Za-z\s]+) ([\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+ [\?\d]+)/) {
    $defenseurs=${1};
    push(@units,split(" ",${2}));
    
}
my @ressources;
if ($text =~ /Ressources \w+ :\s+([\?\d]+)\s+([\?\d]+)\s+([\?\d]+)\s+([\?\d]+)\s+([\?\d]+)/) {
    @ressources=($1,$2,$3,$4,$5);
}
print "$attaquants attaque $defenseurs le $date.\n";
print "Ressources pillées: ";
my $c=0;
foreach (@ressources) {
    print "$_ ".$resnames[$c]."; ";
    $c++;
}
print "\n";
$c=0;
print "             Attaquant     Défenseur\n";
print "Unité        Envoyé Tué    Envoyé Tué\n";
foreach (@units) {
    print $unitnames[int($c/4)]." " if ($c%4==0);
    print "$_"." "x(7-length($_));
    print "\n" if ($c%4==3);
    $c++;
}
