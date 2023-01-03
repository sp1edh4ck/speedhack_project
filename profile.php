<!DOCTYPE html>
<html lang="ru-RU">
<head>
    <meta charset="UTF-8">
	<meta http-equiv="content-type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>speedhack profile</title>
    <link rel="stylesheet" href="css/style.css">
	<link rel="stylesheet" href="css/index.css">
	<link rel="stylesheet" href="css/headers.css">
	<link rel="stylesheet" href="css/footer.css">
	<link rel="stylesheet" href="css/profile.css">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<script type="text/javascript" src="https://vk.com/js/api/openapi.js?168"></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
</head>

<body>
    <div class="wrapper">
		<header class="header">
			<div class="header_con">
				<img class="brandLogo" src="images/Logo-pink.png" alt="speedhack">

				<div class="navbar">
					<div class="container">
						<div class="navbar_wrap">
							<div class="hamb">
								<div class="hamb_field" id="hamb">
									<span class="bar"></span>
									<span class="bar"></span>
									<span class="bar"></span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="popup" id="popup"></div>

				<nav class="header_menu">
					<ul class="menu_list" id="menu">
						<li class="menu_item"><a href="https://speedhack.ru/" class="menu_link">ГЛАВНАЯ</a></li>
						<li class="menu_item"><a href="https://speedhack.ru/forum.php" class="menu_link">ФОРУМ</a></li>
						<li class="menu_item"><a href="https://speedhack.ru/market.php" class="menu_link">МАРКЕТ</a></li>
						<li class="menu_item"><a href="https://speedhack.ru/users.php" class="menu_link">КОМАНДА</a></li>
						<li class="menu_item"><a href="https://speedhack.ru/faq/faq-tech.php" class="menu_link">FAQ</a></li>
					</ul>
				</nav>
				
				<!-- <?php
				    if ($_COOKIE['user'] == ''):
				?> -->
				
				<!-- <div class="header_logreg">
					<button onclick="login()" type="button" class="button">Логин</button>
					<script>
						function login(){
							window.location="https://speedhack.ru/sing/sing-in.php";
						}
					</script>
				  	<button onclick="register()" type="button" class="button">Регистрация</button>
					<script>
						function register(){
							window.location="https://speedhack.ru/sing/sing-up.php";
						}
					</script>
				</div> -->
				
				<!-- <?php else: ?> -->
				<!-- <?=$_COOKIE['user']?> -->
				    <div class="user-button">
					    <button class="user-icon">sp1edh4ckkkk</button>
					    <div class="user-button-content">
					  	    <a href="#" style="border-top: 1px solid; border-color: #ff506f; border-top-left-radius: 5px; border-top-right-radius: 5px;">Профиль</a>
					  	    <a href="#">Мои аккаунты</a>
						    <a href="#">Мои покупки</a>
					  	    <a href="https://speedhack.ru/sing/exit.php" style="border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;">Выйти</a>
					    </div>
				    </div>
				
				<!-- <?php endif; ?> -->
			</div>
		</header>

		<div class="main">
			<div class="frame-profile-avatar_con">
				<img class="profile-avatar" src="images/default avatar.jpg" alt="speedhack">
				<button class="button">Редактировать</button>
			</div>
			<div class="frame-profile-info">
				<span style="color: gray; padding-right: 600px;"><?=$_COOKIE['user']?></span>
				<span style="color: gray;">В сети 10 мин. назад</span>
				<hr style="margin-top: 20px; margin-bottom: 20px;">
				<span style="color: gray;">Регистрация: </span><span style="color: #ffffff;">11 августа 2022</span><br>
				<span style="color: gray;">Ранг: <span style="color: #ffffff;">владелец</span></span>
			</div>
		</div>

		<footer class="footer">
			<ul>
				<a href="https://t.me/sp1edh4ck_project" class="footer-link" target="_blank" style="padding-right: 10px;">Телеграм</a>
				<a href="https://vk.com/sp1edh4ck_project" class="footer-link" target="_blank">ВКонтакте</a>
			</ul>
		  	<hr>
			<p style="color: white;">&copy; 2022 Company, Inc</p>
	  	</footer>
	</div>
	<script type="text/javascript" src="js/barMenu.js"></script>
</body>
</html>