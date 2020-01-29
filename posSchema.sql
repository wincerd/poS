BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `users` (
	`username`	varchar ( 100 ) NOT NULL,
	`userpass`	varchar ( 100 ) NOT NULL,
	`email`	varchar ( 100 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `products` (
	`name`	varchar ( 50 ) NOT NULL,
	`product_num`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`category`	varchar ( 50 ) NOT NULL,
	`description`	varchar ( 50 ) NOT NULL,
	`cog`	INTEGER ( 6 ) NOT NULL,
	`price`	INTEGER ( 6 ) NOT NULL,
	`account`	varchar ( 50 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `journal` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`dat`	varchar ( 50 ) DEFAULT NULL,
	`debit`	varchar ( 11 ) NOT NULL,
	`credit`	varchar ( 11 ) NOT NULL,
	`amount`	INTEGER ( 11 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `contact` (
	`c_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 100 ) DEFAULT NULL,
	`mobile`	INTEGER ( 11 ) DEFAULT NULL,
	`type`	varchar ( 20 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `Account` (
	`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	text,
	`typ`	varchar ( 20 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `contact` (
        `c_id` INTEGER PRIMARY KEY AUTOINCREMENT,
        `name`  varchar( 100 ) DEFAULT NULL,
        `mobile` INTEGER( 11 ) DEFAULT NULL,
        `type` varchar( 20 ) NOT NULL
);
CREATE TABLE IF NOT EXISTS `journal` (
        `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `dat` varchar(50) DEFAULT NULL,
        `debit` varchar(11) NOT NULL,
        `credit` varchar(11) NOT NULL,
        `amount` INTEGER(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS `products` (
        `name` varchar(50) NOT NULL,
        `product_num` INTEGER PRIMARY KEY AUTOINCREMENT,
        `category` varchar(50) NOT NULL,
        `description` varchar(50) NOT NULL,
        `cog` INTEGER(6) NOT NULL,
        `price` INTEGER(6) NOT NULL,
        `account` varchar(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS `sale` (
        `ID` INTEGER PRIMARY KEY AUTOINCREMENT,
        `item` varchar(50) NOT NULL,
        `data` varchar(50) NOT NULL,
        `description` varchar(50) NOT NULL,
        `size` INTEGER(6) NOT NULL,
        `Date` INTEGER(50) NOT NULL,
        `amount` INTEGER(6) NOT NULL
);
COMMIT;
