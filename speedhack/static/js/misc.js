const burgerBtn = document.getElementById("burgerBtnId")
const burgerMenu = document.getElementById("burgerMenuId")

burgerBtn.onclick = function () {
  // burgerMenu.style.display = 'block'
  // burgerMenu.style.translate = 'translate-x(0);'
  burgerMenu.classList.add('bg-open')
}

window.addEventListener('keydown', (event) => {
  if (event.key === "Escape") {
    burgerMenu.classList.remove('bg-open')
  }
})

burgerMenu.addEventListener('click', event => {
  event._isClickWithInModal = true
})

burgerMenu.addEventListener('click', event => {
  if (event._isClickWithInModal) return
  event.currentTarget.classList.remove('bg-open')
})



const modalWindow = document.getElementById("modal-w-topic")
const modalOpenBtn = document.getElementById("modal-w-open")
const modalCloseBtn = document.getElementById("modal-w-close")
const modalOverlay = document.getElementById("modal-w-overlay")

modalOpenBtn.onclick = function () {
  modalWindow.classList.add("mw-topic-active")
  modalOverlay.style.display = 'block'
  document.body.style.overflow = 'hidden'
  document.body.style.opacity = '0.7'
}

modalCloseBtn.onclick = function () {
  modalWindow.classList.remove("mw-topic-active")
  modalOverlay.style.display = 'none'
  document.body.style.overflow = 'scroll'
  document.body.style.opacity = '1'
}
