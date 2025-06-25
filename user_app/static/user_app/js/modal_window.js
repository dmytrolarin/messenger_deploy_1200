const avatar = document.querySelector("#avatar")
const cross = document.querySelector("#cross")
const modalWindow = document.querySelector("#modalWindow")

avatar.addEventListener("click", (event) => {
    modalWindow.classList.add("open") 
})

cross.addEventListener("click", (event) => {
    modalWindow.classList.remove("open")
})