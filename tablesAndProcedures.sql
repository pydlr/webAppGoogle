################################################   STUFF  ##############################
############## SQL DATA TYPES:
https://www.w3schools.com/sql/sql_datatypes.asp

############# START MYSQL SERVICE
Ubuntu:
sudo /etc/init.d/mysql - root -p start

OSX
mysql.server start

############# Google cloud platform SQL instance connection
Google Cloud MySQL instances
connection name:
abogangster-182717:europe-west3:boletin
IPv4:
35.198.153.160
DataBase:
Boletin0


#Access Google Cloud Platform SQL instance from local Shell
mysql --host=35.198.153.160 --user=root --password

Access SQL instance directly from the GCP shell:
gcloud sql connect boletin --user=root
boletin = name of instance
password = abogangster

my local IPv4:
1234.1234.1234.1234


################################################   STUFF  ##############################


################################################   PROCEDURES  ##############################
DELIMITER //
CREATE PROCEDURE `sp_create_user`(
    IN p_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_password VARCHAR(127)
)
BEGIN
    if (( select exists (select 1 from userinfo where user_username = p_username) ) OR ( select exists (select 1 from userinfo where user_name = p_name) )) THEN
        select 'User Exists!';
    ELSE 
        insert into userinfo
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;             
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `sp_insert_usercase`(
    IN p_expediente VARCHAR(16),
    IN p_name VARCHAR(45),
    IN p_location TINYTEXT
)
BEGIN
    if (( select exists (select 1 from usercases where user_name = p_name) ) AND ( select exists (select 1 from usercases where no_expediente = p_expediente) ) )THEN
     
        select 'Name and Case already resgistered !';
     
    ELSE

        insert into usercases
        (
            no_expediente,
            user_name,
            user_location
        )
        values
        (
            p_expediente,
            p_name,
            p_location
        );
        
     
    END IF;             
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `sp_delete_usercase`(
    IN p_expediente VARCHAR(16),
    IN p_name VARCHAR(45),
    IN p_location TINYTEXT
)
BEGIN
    delete from usercases where no_expediente = p_expediente and user_name = p_name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE `sp_delete_user`(
    IN p_name VARCHAR(45)
)
BEGIN
    delete from userinfo where user_name = p_name;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(45)
)
BEGIN
    select * from userinfo where user_username = p_username;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(45)
)
BEGIN
    select * from userinfo where user_username = p_username;
END //
DELIMITER ;

################################################   PROCEDURES  ##############################

################################################   COMMANDS  ##############################
# With no repetition
SELECT distinct no_expediente FROM usercases WHERE user_name = '" + str(name) + "' ORDER BY no_expediente;

# Delete procecure
DROP PROCEDURE IF EXISTS procedureName;

# Delete all from a table
DELETE FROM table_name;

# Restart Autoincrement:
ALTER TABLE tablename AUTO_INCREMENT = 1

# Example
SELECT * FROM `resoluciones` WHERE `autoridad` LIKE '%{$MEXICALI}%'

# restart numeration
restart key autoincrement mysql
################################################   COMMANDS  ##############################



################################################   CREATE TABLES  ##############################
CREATE TABLE `demo_users`.`userinfo` (
  `user_id` BIGINT AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL,
  `user_username` VARCHAR(45) NULL,
  `user_password` VARCHAR(127) NULL,
  PRIMARY KEY (`user_id`));


CREATE TABLE `demo_users`.`usercases` (
  `case_id` BIGINT AUTO_INCREMENT,
  `no_expediente` VARCHAR(16) NULL,
  `user_name` VARCHAR(45) NULL,
  `user_location` TINYTEXT NULL,
  PRIMARY KEY (`case_id`));


CREATE TABLE resoluciones (
    autoridad TINYTEXT, 
    ramo_secretaria TINYTEXT, 
    sala_secretaria TINYTEXT, 
    tipo VARCHAR(48), 
    no_resolucion VARCHAR(8), 
    no_expediente VARCHAR(16), 
    contenido TEXT);
################################################   CREATE TABLES  ##############################





