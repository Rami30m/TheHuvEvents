
document.getElementById('close').addEventListener("click", function() {
    let form = document.getElementById("addForm");
    form.classList.add("close");
})

document.getElementById('No').addEventListener("click", function() {
    let form = document.getElementById("deleteForm");
    form.classList.add("close");
})

document.querySelectorAll(".warn-btn").forEach(function(button) {
    button.addEventListener('click', function() {
        let form = document.getElementById("deleteForm");
        let eventId = this.id;
        form.classList.remove("close");

        let confirmBtn = document.getElementById("event-btn");
        confirmBtn.setAttribute("data-event-id", eventId);
    })
})

document.getElementById("event-btn").addEventListener("click", function() {
    let eventId = this.getAttribute("data-event-id");

    fetch(`/admin-panel/delete/?event_id=${eventId}`, {
        method: 'DELETE',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ event_id: eventId })
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert("Ивент успешно удалён!");
            location.reload();  // Перезагрузить страницу
        } else {
            alert("Ошибка: " + data.error);
        }
    }).catch(error => console.error("Ошибка:", error));
})

document.getElementById("addEvent").addEventListener("click", function() {
    let form = document.getElementById("addForm");
    console.log('открыто');
    form.classList.remove("close");
})

document.getElementById('submit').addEventListener("click", function(e) {
    e.preventDefault();

    let formData = new FormData(); // Используем одинаковое название
    formData.append("title", document.getElementById("title").value);
    formData.append("description", document.getElementById("description").value);
    formData.append("date", document.getElementById("date").value);
    formData.append("location", document.getElementById("location").value);
    formData.append("image", document.getElementById("image").files[0]);

    fetch("/admin-panel/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert("Событие успешно добавлено!");
            location.reload();
        } else {
            alert("Ошибка: " + data.error);
        }
    })
        .catch(error => console.error("Ошибка:", error));
});


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

