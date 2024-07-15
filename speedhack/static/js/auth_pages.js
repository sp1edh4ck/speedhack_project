var form = document.getElementById('login_form')
var username = document.getElementById('id_username')
var email = document.getElementById('id_email')
var password = document.getElementById('id_password1')
var fields = document.querySelectorAll('.input-box')


var generateError = function (text) {
  var error = document.createElement('div')
  error.className = 'error'
  error.style.color = 'red'
  error.innerHTML = text
  return error
}


var removeValidation = function () {
  var errors = form.querySelectorAll('.error')
  for (var i = 0; i < errors.length; i++) {
    errors[i].remove()
  }
}


function inputs_check() {
  for (var i = 0; i < fields.length; i++) {
    if (!fields[i].value) {
      var error = generateError('Обязательное поле')
      form[i].parentElement.insertBefore(error, fields[i])
    }
  }
  // if (fields[0] != '') {
  //   if (fields[1] != '') {
  //     if (fields[2] != '') {
  //       return true
  //     } else {
  //       var error = generateError('Обязательное поле')
  //       password.parentElement.insertBefore(error, password)
  //     }
  //   } else {
  //     var error = generateError('Обязательное поле')
  //     email.parentElement.insertBefore(error, email)
  //   }
  // } else {
  //   var error = generateError('Обязательное поле')
  //   username.parentElement.insertBefore(error, username)
  // }
}


function username_check(username, u_obj) {
  if (username != '') {
    if (username.length <= 2) {
      var error = generateError('username должен быть длиннее 2-х символов')
      u_obj.parentElement.insertBefore(error, u_obj)
    }
  } else {
    var error = generateError('Вы ничего не ввели')
    u_obj.parentElement.insertBefore(error, u_obj)
  }
}


function email_check(email, e_obj) {
  if (email != '') {
    if (email.length <= 2) {
      var error = generateError('username должен быть длиннее 2-х символов')
      e_obj.parentElement.insertBefore(error, e_obj)
    }
  } else {
    var error = generateError('Вы ничего не ввели')
    e_obj.parentElement.insertBefore(error, e_obj)
  }
}


const beginNotDigit = /^\D.*$/
const withoutSpecialChars = /^[^-() ]*$/
const containсLetters = /^.*[a-zA-Z]+.*$/
const minimum8Chars = /^.{8,}$/
const withoutSpaces = /^[\S]$/


function password_check(password, p_obj) {
  if (
    beginNotDigit.test(password) &&
    withoutSpecialChars.test(password) &&
    containсLetters.test(password) &&
    minimum8Chars.test(password) &&
    withoutSpaces.test(password)
  ) {
    form.submit()
  } else {
    var error = generateError('Пароль должен содержать')
    p_obj.parentElement.insertBefore(error, p_obj)
  }
}


form.addEventListener('submit', function (event) {
  event.preventDefault()
  removeValidation()
  inputs_check()
  username_check(username.value, username)
  email_check(email.value, email)
  password_check(password.value, password)
  }
)


function politics_check() {
  var submit = document.getElementById('submit_login_btn')
  if (document.getElementById('politics').checked) {
    submit.disabled = '';
  } else {
    submit.disabled = 'disabled';
  }
}
