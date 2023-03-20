// function myFunction() {
// 	document.getElementById("myDropdown").classList.toggle("show");
// }

// window.onclick = function(e) {
// 	if (!e.target.matches('.dropbtn')) {
// 		var myDropdown = document.getElementById("myDropdown");

// 		if (myDropdown.classList.contains('show')) {
// 			myDropdown.classList.remove('show');
// 		}
// 	}
// }

function myFunction() {
	document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
	var modal = document.getElementById("myModal");
	if (event.target == modal) {
		openDropdown.classList.remove('show');
	}
	if (!event.target.matches('.dropbtn')) {	
		var dropdowns = document.getElementsByClassName("window-other");
		var i;

		for (i = 0; i < dropdowns.length; i++) {
			var openDropdown = dropdowns[i];

			if (openDropdown.classList.contains('show')) {
				openDropdown.classList.remove('show');
			}
		}
	}
}