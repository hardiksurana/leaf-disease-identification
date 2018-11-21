create database leafDiseaseIdentification;

use leafDiseaseIdentification;

create table register(name varchar(30) NOT NULL, 
email varchar(30) NOT NULL,
username varchar(20) PRIMARY KEY,
password varchar(20) NOT NULL
);

create table Login(username varchar(20),
password varchar(20) NOT NULL,
FOREIGN KEY (username) REFERENCES register (username),
PRIMARY KEY(username)
);
