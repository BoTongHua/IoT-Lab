-- Usunięcie istniejącej bazy danych o tej samej nazwie, jeśli istnieje
DROP DATABASE IF EXISTS parking_db;

-- Utworzenie nowej bazy danych
CREATE DATABASE parking_db;

-- Użycie nowo utworzonej bazy danych
USE parking_db;

-- Tworzenie tabeli aktualne_wjazdy
CREATE TABLE aktualne_wjazdy (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Klucz główny, automatyczne numerowanie
    rfid_id VARCHAR(255) NOT NULL,            -- ID karty RFID
    data_wjazdu DATETIME NOT NULL             -- Czas wjazdu
);

-- Tworzenie tabeli archiwum
CREATE TABLE archiwum (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- Klucz główny, automatyczne numerowanie
    rfid_id VARCHAR(255) NOT NULL,            -- ID karty RFID
    data_wjazdu DATETIME NOT NULL,            -- Czas wjazdu
    data_wyjazdu DATETIME NOT NULL            -- Czas wyjazdu
);

-- Dodanie przykładowego użytkownika bazy danych z pełnymi uprawnieniami
CREATE USER IF NOT EXISTS 'parking_user'@'%' IDENTIFIED BY 'secure_password';

-- Przyznanie użytkownikowi pełnych uprawnień do bazy danych parking_db
GRANT ALL PRIVILEGES ON parking_db.* TO 'parking_user'@'%';

-- Zatwierdzenie zmian w uprawnieniach
FLUSH PRIVILEGES;
