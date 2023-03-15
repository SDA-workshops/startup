create schema if not exists startup;

use startup;

create table if not exists departments
(
    id         int auto_increment primary key,
    name       varchar(50) not null,
    address    varchar(50) not null,
    manager_id varchar(20) not null
);

create table if not exists employees
(
    pesel        varchar(20)  not null primary key,
    last_name    varchar(50)  not null,
    first_name   varchar(50)  not null,
    email        varchar(50)  not null,
    birth        date         not null,
    phone        varchar(20)  not null,
    home_address varchar(100) not null
);

create table if not exists employees_departments
(
    employee_id   varchar(20) not null,
    department_id int         not null,
    date          date        not null,
    primary key (employee_id, department_id)
);

create table if not exists employees_positions
(
    employee_id varchar(20) not null,
    position_id int         not null,
    date        date        not null,
    primary key (employee_id, position_id)
);

create table if not exists managers_departments
(
    employee_id varchar(20) not null,
    manager_id  int         not null,
    date        date        not null,
    primary key (employee_id, manager_id)
);

create table if not exists positions
(
    id            int auto_increment
        primary key,
    name          varchar(20) not null,
    amount        decimal     not null,
    department_id int         not null
);

create table if not exists salaries
(
    id     int auto_increment primary key,
    amount decimal     not null,
    date   date        not null,
    pesel  varchar(20) not null
);
