function showInfo(title, x, y, imagePath, scanned = false, info = null) {
    document.getElementById('popup-title').textContent = title;
    document.getElementById('popup-x').textContent = `X: ${x}`;
    document.getElementById('popup-y').textContent = `Y: ${y}`;

    const description = document.getElementById('popup-description');
    if (scanned && info) {
        description.textContent = info;
    } else {
        description.textContent = "Объект не разведан. Отправьте дрона.";
    }

    const popup = document.getElementById('info-popup');

    popup.style.backgroundImage = `
        linear-gradient(to right, black 0%, rgba(0,0,0,0.95) 20%, rgba(0,0,0,0.6) 40%, rgba(0,0,0,0.2) 70%, rgba(0,0,0,0) 100%),
        url('${imagePath}')
    `;

    popup.style.backgroundSize = 'cover';
    popup.style.backgroundPosition = 'center right';
    popup.style.backgroundRepeat = 'no-repeat';

    popup.style.display = 'block';
}

function hideInfo() {
    document.getElementById('info-popup').style.display = 'none';
}

function toggleCoords() {
    const coordsDisplay = document.getElementById('coords-display');
    coordsDisplay.style.display = coordsDisplay.style.display === 'none' ? 'block' : 'none';
}
const map = document.getElementById('map');
const coordsDisplay = document.getElementById('coords-display');

map?.addEventListener('mousemove', (event) => {
    const rect = map.getBoundingClientRect();
    const x = Math.floor(event.clientX - rect.left);
    const y = Math.floor(event.clientY - rect.top);
    coordsDisplay.textContent = `X: ${x}, Y: ${y}`;
});
function switchLocation(direction) {
    const label = document.getElementById("mode-label");
    const droneIcon = document.getElementById("drone-toggle");
    const form = document.getElementById("drone-form");

    if (direction === 1) {
        label?.classList.remove("active");
        droneIcon?.classList.add("active");
        form.style.display = "block";
    } else {
        label?.classList.add("active");
        droneIcon?.classList.remove("active");
        form.style.display = "none";
    }
}
