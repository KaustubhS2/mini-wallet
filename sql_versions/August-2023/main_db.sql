CREATE DATABASE miniwallet;
USE miniwallet;

--DROP TABLE wallets;

CREATE TABLE wallets (
    id VARCHAR(36) PRIMARY KEY,
    owned_by VARCHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,
    enabled_at DATETIME NOT NULL,
    balance FLOAT NOT NULL DEFAULT 0
);

CREATE TABLE transactions (
    id VARCHAR(36) NOT NULL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    status VARCHAR(20) NOT NULL,
    transacted_at DATETIME NOT NULL,
    type VARCHAR(20) NOT NULL,
    amount FLOAT NOT NULL,
    reference_id VARCHAR(36) NOT NULL
);

