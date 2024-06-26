#!/usr/bin/perl

use CGI;
use CGI::Session;
use Sudo;

my $cgi = new CGI;
my $session= new CGI::Session;

$session->load();
my @args = $session->param;

if ($session->is_expired or @args eq 0){
        $session->delete();
        $session->flush();

        print $cgi->redirect("https://avanzaii");
}else{

        my $flag = 0;
        my $username = $session->param("username");
        my $directory = "/home/$username";

        opendir (DIR, $directory) or die $!;

        while (my $file = readdir(DIR)) {

                if ($file eq "pagina_personal"){
                        $flag=1;
                        last;
                }

        }
        closedir(DIR);
        if ($flag)
        {
                my $args = "/home/$username/pagina_personal /home/$username/public_html";

                my $sudo_mv = Sudo->new({
                        sudo         => '/usr/bin/sudo',
                        username     => 'root',
                        password     => 'compu',
                        program      => '/bin/mv',
                        program_args => $args,
                });

                my $result = $sudo_mv->sudo_run();
        }
        print $cgi->redirect("https://avanzaii/profile.html");
}
