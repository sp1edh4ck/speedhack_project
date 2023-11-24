const tabs = document.querySelectorAll(".switch-button");
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
