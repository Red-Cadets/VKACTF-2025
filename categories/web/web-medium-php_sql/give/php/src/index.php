<?php

session_start();

if (!isset($_SESSION['user_id'])) {
    $_SESSION['user_id'] = bin2hex(random_bytes(8));
}

$user_id = $_SESSION['user_id'];

$pdo = new PDO("sqlite:" . __DIR__ . "/data/db.sqlite");
$objectsStmt = $pdo->prepare("
    SELECT o.name, o.x, o.y, o.info, o.image, s.object_id IS NOT NULL AS scanned
    FROM objects o
    LEFT JOIN scans s ON s.object_id = o.id AND s.user_id = :user_id
");
$objectsStmt->execute([':user_id' => $user_id]);
$objects = $objectsStmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title><?= htmlspecialchars($currentLocation) ?></title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="map-container">
        <img id="map" src="assets/maps/map.jpg" class="map">

        <?php foreach ($objects as $obj): ?>
            <img 
                class="map-object" 
                src="assets/images/button.jpg"
                style="left: <?= (int)$obj['x'] ?>px; top: <?= (int)$obj['y'] ?>px;" 
                alt="<?= htmlspecialchars($obj['name']) ?>"
                onclick='showInfo(
                    <?= json_encode($obj["name"]) ?>,
                    <?= (int)$obj["x"] ?>,
                    <?= (int)$obj["y"] ?>,
                    <?= json_encode("assets/images/" . $obj["image"]) ?>,
                    <?= $obj["scanned"] ? "true" : "false" ?>,
                    <?= $obj["scanned"] ? json_encode($obj["info"]) : "null" ?>
                )'
            >
        <?php endforeach; ?>

        <div id="info-popup" class="popup">
            <div class="popup-overlay">
                <div class="popup-content">
                    <div class="popup-header">
                        <div class="popup-title" id="popup-title">Название</div>
                        <button onclick="hideInfo()" style="float: right; background: none; border: none; font-size: 20px; cursor: pointer;">✖</button>
                    </div>
                    <div class="popup-description" id="popup-description">Описание объекта</div>
                    <div class="popup-coords">
                        <span id="popup-x">X: 0</span>
                        <span id="popup-y">Y: 0</span>
                    </div>
                    <div class="location-label">МЕСТО НАХОЖДЕНИЯ</div>
                </div>
            </div>
        </div>
    </div>

    <div class="location-bar">
        <button class="scroll-button left" id="btn-left" type="button">
            <img src="assets/images/key_q_upper_case.svg" alt="Q">
        </button>
        <a id="mode-label" class="active">Карта</a>
        <a id="drone-toggle" >Дрон-разведчик</a>
        <button class="scroll-button right" id="btn-right" type="button">
            <img src="assets/images/e_upper_case_key.svg" alt="E">
        </button>
    </div>

    <div id="drone-form" class="drone-form">
    <div class="drone-header">
        <img src="assets/images/drone.jpg" class="drone-image">
        <h3>ДРОН-РАЗВЕДЧИК СИПУХА</h3>
    </div>
    <div id="drone-status" style="display: none; color: white;"></div>

    <form id="drone-coords-form" class="drone-form-content" onsubmit="sendDrone(event)">
        <label for="drone-x">КООРДИНАТА X:</label>
        <input type="number" id="drone-x" name="x" required class="drone-input">
        
        <label for="drone-y">КООРДИНАТА Y:</label>
        <input type="number" id="drone-y" name="y" required class="drone-input">

        <label for="location">ЛОКАЦИЯ:</label>
        <input type="text" id="location" name="location" required class="drone-input">
        
        <div class="drone-buttons">
            <button type="submit" class="drone-submit">ОТПРАВИТЬ</button>
            <button type="button" onclick="toggleDroneForm()" class="drone-cancel">ОТМЕНА</button>
        </div>
    </form>
</div>
<div id="coords-display" style="
    position: absolute;
    bottom: 20px;
    left: 20px;
    color: white;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 5px;
    font-family: monospace;
    display: block;
">
    X: 0, Y: 0
</div>
<script src="assets/js/ui.js" defer></script>
<script src="assets/js/drone.js" defer></script>
</body>
</html>