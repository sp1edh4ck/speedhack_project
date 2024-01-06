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


var buttons = document.querySelectorAll('.rrft');
var contents = document.querySelectorAll('.edit-form-user');

buttons.forEach(function(button, index) {
  button.addEventListener('click', function() {
    if (contents[index].style.minHeight === '0px' || contents[index].style.minHeight === '') {
        contents[index].style.minHeight = '900px';
        buttons[index].style.transform = 'rotate(180deg)';
    } else {
      contents[index].style.minHeight = '0px';
      buttons[index].style.transform = 'rotate(0deg)';
    }
  });
});



// const menu_user_edit = document.querySelector('#menu_user_edit');
// const js_menu_user_edit = document.querySelector('.edit-form-user-size');

// menu_user_edit.addEventListener('click', function(e) {
// 	e.preventDefault();
// 	menu_user_edit.classList.toggle('active-menu');
// 	js_menu_user_edit.classList.toggle('active-menu');
// });
