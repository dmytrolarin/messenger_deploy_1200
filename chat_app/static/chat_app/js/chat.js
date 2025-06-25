/*
    Файл для взаємодії клієнта з сервером за протоколом WS
*/

// Отримуємо id групи з спеціального тегу
const groupId = document.getElementById('groupId').value
// Формуємо URL адресу для WS-з'єднання за поточним хостом
const SOCKET_URL = `ws://${window.location.host}/chat/${groupId}`
// Ініціалізуємо WebSocket (Створюємо WS-з'єднання)
const CHAT_SOCKET = new WebSocket(SOCKET_URL)

// Після успішного з'єднання повідомлення виводится у консоль
CHAT_SOCKET.addEventListener("open",() => console.log("Успішне з`єднання"))

// Створюємо функцію, яка відповідає за опрацьовання часу під часовий пояс користувача з переданого тексту (дати)
function processMessageTime(text){
    // Створюємо об'єкт дати, користуючись інформацією про дату, котру передавали в функцію
    let date = new Date(text)
    // Перетворюємо об'єкт дати у рядок, котру користувач може читати, додатково локалізуючи згідно з налаштуваннями системи
    let dateText = date.toLocaleString();
    // Повертає текст часу
    return dateText
}

// Отримуємо всі часи відправлень повідомлень
const messageTimes = document.querySelectorAll(".message-time")
// Перебираємо всі часи повідомлень
for (let messageTime of messageTimes){
    // Отримуємо дату/текст з елементу часу повідомлення
    let text = messageTime.textContent
    // Встановлюємо новий час у елемент часу повідомлення з локалізованим часом
    messageTime.textContent = processMessageTime(text)
}

// Отримуємо DOM-елемент, в який будуть додаватися нові повідомлення
const messages = document.getElementById("messages");
// Слухаємо події надходження повідомлень від WebSocket-з'єднання
CHAT_SOCKET.addEventListener("message", (event) => {
    // Розбираємо отриманий JSON-рядок у вигляді об'єкта
    let data = JSON.parse(event.data);
    // Локалізуємо час, котрий був передан до клієнта, під часовий пояс користувача
    let localTime = processMessageTime(data.datetime)
    // Додаємо нове повідомлення до вмісту блоку з повідомленнями
    messages.innerHTML += `<p>${data.message} (${localTime})</p>`;
})

// Створюємо константу messageForm з об'єктом форми
const messageForm = document.querySelector("#messageForm");
// Створюємо константу messageTextInput об'єктом поля з повідомленням
const messageTextInput = document.querySelector("#id_message");
// Прослуховування подію відправки форми
messageForm.addEventListener("submit", (event) => {
    // Зупиняємо дію за замовучванням (відправку форми)
    event.preventDefault();
    // Створюємо змінну message й задаємо значення з константи messageTextInput
    let message = messageTextInput.value;
    // Створюємо об'єкт для відправки на клієнт
    let dataToSend = {"message": message};
    // Створюємо JSONString та перетворюємо його в string
    let JSONString = JSON.stringify(dataToSend);
    // Відправляємо JSONString на сервер
    CHAT_SOCKET.send(JSONString);
    // Очищуємо messageForm без оновлення сторінки
    messageForm.reset()
}
)
