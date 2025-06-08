<?php
session_start();

header('Content-Type: application/json');
$pdo = new PDO("sqlite:" . __DIR__ . "/data/db.sqlite");
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$contentType = $_SERVER['CONTENT_TYPE'] ?? '';

if (stripos($contentType, 'application/octet-stream') !== false) {
    $handle = fopen("php://input", "r");
    $location = '';
    while ($data = fread($handle, 8192)) {
        $location .= $data;
    }
    fclose($handle);
    $x = $_GET['x'] ?? null;
    $y = $_GET['y'] ?? null;
} else {
    $location = $_POST['location'] ?? '';
    $x = $_POST['x'] ?? null;
    $y = $_POST['y'] ?? null;

    $max_length = 1000000;
    $fields = ['location' => $location, 'x' => $x, 'y' => $y];

    foreach ($fields as $name => $value) {
        if ($value !== null && strlen($value) > $max_length) {
            echo json_encode([
                'status' => 'error',
                'message' => "Оперативная память дрона переполнена — данные поля «$name» слишком велики для стандартного POST-запроса."
            ]);
            exit;
        }
    }
}

$quotedInput1 = $pdo->quote($location);
$quotedInput2 = $pdo->quote($x);
$quotedInput3 = $pdo->quote($y);

$sql = "SELECT id,name,info,image FROM objects WHERE name = $quotedInput1 AND x = $quotedInput2 AND y = $quotedInput3";

try {
    $stmt = $pdo->query($sql);
    $object = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($object) {
        echo json_encode([
            'status' => 'found',
            'name' => $object['name'],
            'image' => $object['image'],
            'info' => $object['info']
        ]);
        $stmt = $pdo->prepare("INSERT OR IGNORE INTO scans (user_id, object_id) VALUES (:user_id, :object_id)");
        $stmt->execute([
            ':user_id' => $_SESSION['user_id'],
            ':object_id' => $object['id']
        ]);

    } else {
        echo json_encode([
            'status' => 'not_found',
            'message' => 'Дрон не обнаружил ничего полезного.'
        ]);
    }
} catch (PDOException $e) {
    echo json_encode([
        'status' => 'error',
        'message' => "Ошибка: " . htmlspecialchars($e->getMessage())
    ]);
}
?>
