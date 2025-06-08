function showFormPopup(obj) {
    let text;
    if (typeof obj === "object" && obj !== null) {
        text = obj.text || "";
    } else {
        text = obj + "";
    }
    let alert = document.getElementById("form-popup-alert");
    alert.innerText = text;
    alert.style.display = "block";
    setTimeout(() => { alert.style.display = "none"; }, 4500);
}

const ITEM_IMAGES = {
    "algo": "/static/img/algo.png",
    "pesticide": "/static/img/pesticide.png",
    "hot": "/static/img/hot.png",
    "cold": "/static/img/cold.png"
};

function checkAndRunPolymerAnimation(inv) {
    if (
        inv["algo"] &&
        inv["pesticide"] &&
        inv["hot"] &&
        inv["cold"] &&
        !window.__polymer_animation_ran__
    ) {
        window.__polymer_animation_ran__ = true;
        setTimeout(() => {
            showFormPopup("Запускаю процесс полимеризации...");

            setTimeout(() => {
                runPolymerShaderAnimation();
            }, 3000);
        }, 1000);
    }
}

function updateInventoryFromBackend() {
    fetch("/get_inventory")
        .then(r => r.json())
        .then(inv => {
            for (let i = 1; i <= 4; ++i) {
                const slot = document.getElementById('slot-' + i);
                if (slot) slot.innerHTML = '';
            }
            let order = inv.order || [];
            order.forEach((key, idx) => {
                if (idx < 4 && ITEM_IMAGES[key]) {
                    const slot = document.getElementById('slot-' + (idx + 1));
                    if (slot) {
                        const img = document.createElement('img');
                        img.src = ITEM_IMAGES[key];
                        img.alt = key;
                        slot.appendChild(img);
                    }
                }
            });
            checkAndRunPolymerAnimation(inv);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    updateInventoryFromBackend();
});