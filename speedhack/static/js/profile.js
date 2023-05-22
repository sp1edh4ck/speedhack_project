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


var depModal = document.getElementById("depModal");
var depBtn = document.getElementById("depBtn");
var depSpan = document.getElementsByClassName("close")[0];

depBtn.onclick = function() {
	depModal.style.display = "block";
}

depSpan.onclick = function() {
	depModal.style.display = "none";
}

window.onclick = function(event) {
	if (event.target == depModal) {
		depModal.style.display = "none";
	}
}

var infoModal = document.getElementById("infoModal");
var infoBtn = document.getElementById("infoBtn");
var infoSpan = document.getElementsByClassName("close")[1];

infoBtn.onclick = function() {
	infoModal.style.display = "block";
}

infoSpan.onclick = function() {
	infoModal.style.display = "none";
}

window.onclick = function(event) {
	if (event.target == infoModal) {
		infoModal.style.display = "none";
	}
}


let fields = document.querySelectorAll('.field-load');
Array.prototype.forEach.call(fields, function (input) {
	let label = input.nextElementSibling,
	labelVal = label.querySelector('.file-load').innerText;

input.addEventListener('change', function (e) {
	let countFiles = '';
	if (this.files && this.files.length >= 1)
		countFiles = this.files.length;

if (countFiles)
	label.querySelector('.file-load').innerText = 'Выбрано файлов: ' + countFiles;
else
	label.querySelector('.file-load').innerText = labelVal;
	});
});
