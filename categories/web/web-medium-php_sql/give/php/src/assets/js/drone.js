let droneMode = false;
function toggleDroneForm() {
    droneMode = !droneMode;

    const label = document.getElementById("mode-label");
    const droneIcon = document.getElementById("drone-toggle");
    const form = document.getElementById("drone-form");

    if (droneMode) {
        label?.classList.remove("active");
        droneIcon?.classList.add("active");
        form.style.display = "block";
    } else {
        label?.classList.add("active");
        droneIcon?.classList.remove("active");
        form.style.display = "none";
    }
}

document.getElementById("drone-toggle")?.addEventListener("click", toggleDroneForm);

document.addEventListener("keydown", (event) => {
    if (event.key === "e" || event.key === "q") {
        toggleDroneForm();
    }
});
function sendDrone(event) {
    event.preventDefault();

    const form = event.target;
    const x = form.x.value;
    const y = form.y.value;
    const locationValue = form.location.value;  
    const statusDiv = document.getElementById('drone-status');
    statusDiv.textContent = "Дрон вылетел на координаты...";
    statusDiv.style.display = 'block';

    fetch("drone.php", {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `x=${encodeURIComponent(x)}&y=${encodeURIComponent(y)}&location=${encodeURIComponent(locationValue)}`
    })
    .then(res => res.json()) 
    .then(data => {
        if (data.status === 'found') {
            statusDiv.textContent = "Дрон вернулся с разведданными...\n...Информация на карте обновлена...";

            showInfo(
                data.name,
                x,
                y,
                `assets/images/${data.image}`,
                true,
                data.info
            );

            setTimeout(() => {
                location.reload(); 
            }, 1000);
        } else {
            statusDiv.textContent = "Дрон ничего не обнаружил";
        }
    })
    .catch(error => {
        console.error('Ошибка при запросе данных:', error);
        alert('Произошла ошибка при получении данных с сервера.');
    });
}
