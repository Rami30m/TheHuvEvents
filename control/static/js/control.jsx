// import QrScanner from 'qr-scanner';

let qrResult = "";
const videoElem = document.querySelector("video");
const qrScanner = new QrScanner(
    videoElem,
    result => {qrResult = result; console.log('decoded qr code:', qrResult);
        fetch("/control/", {
            method: 'POST',
            body: JSON.stringify(qrResult),
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }
        }).then(response => response.json())
            .then(data => {
            if (data.find) {
                console.log("QR Найден");
                console.log(data.name);
                document.getElementById("customer").innerHTML = data.name;
                document.getElementById("yet").style.display = "none";
                document.getElementById("success").style.display = "none";
            } else {
                console.log("Ошибка: " + data.error);
            }
        })
            .catch(error => console.error("Ошибка:", error));
        },
    { /* your options or returnDetailedScanResult: true if you're not specifying any other options */ },
);

document.getElementById('play').addEventListener('click', () => {
    qrScanner.start();
})

document.getElementById('stop').addEventListener('click', () => {
    qrScanner.stop();
})

document.getElementById('change').addEventListener('click', () => {

    fetch("/control/change/", {
        method: 'POST',
        body: JSON.stringify(qrResult),
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        }
    }).then(response => response.json()).then(data => {
        if (data.yet) {
            document.getElementById("yet").style.display = "block";
            console.log("Пользователь уже отмечен.");
        } else if (data.success) {
            console.log("Статус изменен");
            document.getElementById("success").style.display = "block";
        } else {
            console.log("Ошибка: " + data.error);
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
