#!/usr/bin/perl
use DBI;

my $db=DBI->connect('dbi:mysql:database=avanzadb;host=localhost','administrator','admin');
my $q = $db->prepare("delete from avanzadb.users where state=1");
$q->execute();
$q->finish();
