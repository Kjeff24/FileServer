
const messageSent = document.querySelector(".message_sent")
const message = document.querySelector(".message")
messageSent.addEventListener("click", function () {
  message.classList.toggle("active");
});
