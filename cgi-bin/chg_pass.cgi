#!/usr/bin/perl

use CGI;
use CGI::Session;
use DBI;
use MIME::Base64;
use Linux::usermod;

my $cgi = new CGI;
my $session= new CGI::Session;

$session->load();
my @args = $session->param;

if ($session->is_expired or @args eq 0){
        $session->delete();
        $session->flush();

        print $cgi->redirect("https://avanzaii");
}else{

        my $O_Pwd = $cgi->param("OPwd");
        my $N_Pwd = $cgi->param("NPwd");
        my $R_Pwd = $cgi->param("NRPwd");
        my $username = $session->param("username");

        if ($N_Pwd ne $R_Pwd){
                print $cgi->redirect("https://avanzaii/ajustes.html");
        }else{
                my $encode = encode_base64($O_Pwd);
                my $db=DBI->connect('dbi:mysql:database=avanzadb;host=localhost','administrator','admin') or die print("<p>el error es".DBI->errstr."</p>");
                my $sth=$db->prepare('SELECT id, is_admin, role FROM users WHERE id=? and password=?') or warn $db->errstr;
                $sth->execute($username, $encode) or die $sth->errstr;

                my @chk_id = $sth->fetchrow_array;
                $sth->finish();

                if(@chk_id){

                        my $user = Linux::usermod->new($username);
                        my $encode_N = encode_base64($N_Pwd);
                        $user->set("password",$N_Pwd);

                        my $q = $db->prepare("update avanzadb.users set password=? where id=?");
                        $q->execute($encode_N,$username);
                        $q->finish();

                        my $role = @chk_id[0];
                        my $admin = @chk_id[1];
                        my $state = @chk_id[2];

                        print $cgi->header();
                        print_propmt();
                        if ($state eq 2 and $admin eq 1){
                                print "<meta http-equiv='Refresh' content='4; /admin.html' />"
                        }elsif($state eq 2){
                                if ($role eq 1){
                                        print "<meta http-equiv='Refresh' content='4; /profesor.html' />"
                                }else{
                                        print "<meta http-equiv='Refresh' content='4; /alumno.html' />"
                                }
                        }else{
                                print "<meta http-equiv='Refresh' content='4; /index.html' />"
                        }
                }
                else{
                        print $cgi->redirect("https://avanzaii/ajustes.html");
                }
        }
}

sub print_propmt{
print '<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>AvanzaII</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <div class="back-div">
        <p><a href="javascript:history.back()"><strong> ← Volver</strong></a></p>
    </div>
    <div class="container2">
        <div class="div-center4">
            <p style="color:black; background-color:white;">Actualización de contraseña realizada correctamente</p>
        </div>
</body>

</html>';
}
