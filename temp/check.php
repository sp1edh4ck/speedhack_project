<?php
    $login = filter_var(trim($_POST['login']), FILTER_SANITIZE_STRING);
    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_STRING);
    $password = filter_var(trim($_POST['password']), FILTER_SANITIZE_STRING);

    $mysql = new mysqli('u1753963_default@localhost', 'u1753963_default', '1DG7F80Van1wkeXH', 'u1753963_users');
    $mysql -> query("INSERT INTO `reg_user` (login, email, password) VALUES($login, $email, $password)");
    $mysql -> close();
?>