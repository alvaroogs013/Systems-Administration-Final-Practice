#!/usr/bin/perl

use CGI;
use CGI::Session;
use DBI;

my $cgi = new CGI;
my $session= new CGI::Session;

$session->load();
my @args = $session->param;

if ($session->is_expired or @args eq 0){
        $session->delete();
        $session->flush();

        print $cgi->redirect("https://avanzaii");
}
else{
        my $username = $session->param("id");
        my $password = $session->param("password");
        # Search the user in the database
        my $db=DBI->connect('dbi:mysql:database=avanzadb;host=localhost','administrator','admin');
        my $sth=$db->prepare('SELECT role, is_admin, state FROM users WHERE id=?') or warn $db->errstr;
        $sth->execute($username) or die $sth->errstr;

        my @user= $sth->fetchrow_array;
        $sth->finish();

        if(@user ne 0){
                my $role = @user[0];
                my $admin = @user[1];
                my $state = @user[2];
                if ($state eq 2 and $admin eq 1){
                        print $cgi->redirect("https://avanzaii/admin.html");
                }elsif($state eq 2){
                        if ($role eq 1){
                                print $cgi->redirect("https://avanzaii/profesor.html");
                        }else{
                                print $cgi->redirect("https://avanzaii/alumno.html");
                        }
                }
                else{
                        print $cgi->redirect("https://avanzaii");
                }       
        }else{
                print $cgi->redirect("https://avanzaii");
        }
}
