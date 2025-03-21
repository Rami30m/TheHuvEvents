document.getElementById('close').addEventListener("click", function() {
    let form = document.getElementById("addForm");
    form.classList.add("close");
})

document.getElementById('close2').addEventListener("click", function() {
    let form = document.getElementById("addForm");
    form.classList.add("close");
    location.reload();
})

document.querySelectorAll(".event-btn").forEach(function(eventCard) {
    eventCard.addEventListener("click", function() {
        let eventId = eventCard.dataset.eventId;
        let title = eventCard.dataset.title;
        let description = eventCard.dataset.description;
        let date = eventCard.dataset.date;
        let location = eventCard.dataset.location;

        // Вставляем данные в форму
        document.getElementById("event-title").innerText = title;
        document.getElementById("event-description").innerText = description;
        document.getElementById("event-date").innerText = date;
        document.getElementById("event-location").innerText = location;


        document.getElementById("event-id").value = eventId;

        let form = document.getElementById("addForm");
        form.classList.remove("close"); // Открываем форму
    });
});

document.getElementById('reg').addEventListener("click", function() {
    let eventId = document.getElementById("event-id").value;
    let name = document.getElementById("event-name").value;
    let Email = document.getElementById("event-email").value;

    console.log("Отправляем данные:", { eventId, name, Email });

    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ event_id: eventId, name: name, email: Email })
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert("Successfully registered!");
            let form = document.getElementById('Form1')
            form.classList.add("сс");

            let form2 = document.getElementById("event-status")
            form2.style.display = "grid";

            document.getElementById("qrImage").src = data.qr_code_url;
        } else if (data.exists) {
            document.getElementById("warn").textContent = "Такие данные уже есть";
        }
    }).catch(error => console.error("Ошибка:", error));
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}