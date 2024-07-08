const input1 = document.getElementById('input1')
const input2 = document.getElementById('input2')
const result = document.getElementById('result')
const subBtn = document.getElementById('submit')
const plusBtn = document.getElementById('plus')
const minusBtn = document.getElementById('minus')
let action = "+"


plusBtn.onclick = function () {
  action = '+'
}


minusBtn.onclick = function () {
  action = '-'
}


function colorResult(sum) {
  if (sum < 0) {
    result.style.color = 'red'
  } else {
    result.style.color = 'green'
  }
  result.textContent = sum
}


function computeNumbers(val1, val2, actionSymbol) {
  const num1 = Number(val1.value)
  const num2 = Number(val2.value)
  return actionSymbol == '+' ? num1 + num2 : num1 - num2
}


subBtn.onclick = function () {
  computeNumbers(input1, input2, action)
  colorResult(sum)
}

