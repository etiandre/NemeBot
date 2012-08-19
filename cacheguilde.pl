use WWW::Mechanize;
use Digest::SHA1;
use YAML qw(DumpFile);
use strict;
use warnings;


my $ua="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1";
my $login="etiandre";
my $password="louloul";


my $guilde=shift; # joueur récupéré dans les arguments du script

my $mech = WWW::Mechanize->new();
$mech->agent($ua);
$mech->get("http://www.nemeria.com/auth");
$mech->submit_form(
	form_number => 1,
	fields => {
		username=>$login,
		password=>"",
        sha1password=>Digest::SHA1::sha1_hex($password),
        remember=>0
	}
);
sub cache {
    my $i=1;
    my $first=-1;
    my %guildes;
    while (1) {
        $mech->get("http://aurora.nemeria.com/classement/alliance?page=$i");
        my $t=$mech->content();
        while ($t =~ /<a href="\/alliance\?id=(\d+)">(.+)<\/a>/g) {
            print "$2 $1\n";
            if ($1==$first) {
                DumpFile("cache/guildes",%guildes);
                return;
            }
            $first=$1 if $first==-1;
            $guildes{$2}=$1;
        }
        $i+=1;
    }
}

cache()
