CREATE TABLE aktualne_wjazdy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rfid_id VARCHAR(255) NOT NULL,
    data_wjazdu DATETIME NOT NULL
);

CREATE TABLE archiwum (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rfid_id VARCHAR(255) NOT NULL,
    data_wjazdu DATETIME NOT NULL,
    data_wyjazdu DATETIME NOT NULL
);
