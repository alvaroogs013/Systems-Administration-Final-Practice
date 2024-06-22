#!/usr/bin/perl

use File::Rotate::Backup;

my $params = { archive_copies => 3,
               dir_copies => 1,
               backup_dir => '/back',
               file_prefix => 'av_back_',
               secondary_backup_dir => '/back2',
               secondary_archive_copies => 3,
               verbose => 0,
               use_flock => 1,
             };

my $backup = File::Rotate::Backup->new($params);

$backup->backup([ ['/home/' => 'home' ],
                  ['/sbin/' => 'sbin' ],
                  ['/etc/skel' => 'etc_skel' ],
                  ['/var/www/' => 'var_www' ],
                  ['/usr/lib/cgi-bin/' => 'usr_lib_cgi-bin' ],
                  ['/var/lib/mysql/' => 'var_lib_mysql' ],
                  ]);
$backup->rotate;
