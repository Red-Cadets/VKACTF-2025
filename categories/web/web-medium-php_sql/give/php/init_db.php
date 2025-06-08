<?php

$dbFile = __DIR__ . '/data/db.sqlite';

@mkdir(__DIR__ . '/data', 0777, true);

$pdo = new PDO("sqlite:" . $dbFile);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$pdo->exec("
    CREATE TABLE IF NOT EXISTS objects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        info TEXT,
        image TEXT,
        flag TEXT
    )
");

$pdo->exec("
    CREATE TABLE IF NOT EXISTS scans (
        user_id TEXT PRIMARY KEY,
        object_id INTEGER,
        FOREIGN KEY(object_id) REFERENCES objects(id)
    )
");

?>
