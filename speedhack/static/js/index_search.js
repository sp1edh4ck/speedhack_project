let input = document.getElementById('input')
let list = document.querySelectorAll('.index-box-search')
let deleteBtn = document.getElementById('delete_id')

deleteBtn.addEventListener('click', function() {
  input.value = ''
  list.forEach(element => {
    element.classList.remove('search-items-hide')
  })
})

window.onload = () => {
  console.log(input.value)
  input.oninput = function () {
    let value = this.value.trim()
    if (value != '') {
      list.forEach(element => {
        if (element.innerText.search(value) == -1) {
          element.classList.add('search-items-hide')
        } else {
          element.classList.remove('search-items-hide')
        }
      })
    } else {
      list.forEach(element => {
        element.classList.remove('search-items-hide')
      })
    }
  }
}