const tabs = document.querySelectorAll(".button-tools");
const tabsItems = document.querySelectorAll(".tabItem");

tabs.forEach(function(item) {
	item.addEventListener("click", function() {
		let currentButton = item;
		let tabId = currentButton.getAttribute("data-tab");
		let currentTab = document.querySelector(tabId);

		if (!currentButton.classList.contains('active-tab')) {
			tabs.forEach(function(item) {
				item.classList.remove('active-tab');
			});
	
		tabsItems.forEach(function(item) {
			item.classList.remove('active-tab');
		});

			currentButton.classList.add('active-tab');
			currentTab.classList.add('active-tab');
		}
	});
});


var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
	modal.style.display = "block";
}

span.onclick = function() {
	modal.style.display = "none";
}

window.onclick = function(event) {
	if (event.target == modal) {
		modal.style.display = "none";
	}
}


$(".arrow-4").click(function() {
	$(this).toggleClass("open");
});
