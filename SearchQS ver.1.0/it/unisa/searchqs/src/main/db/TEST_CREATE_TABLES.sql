USE testsearchqs;

CREATE TABLE `residential_address` (
	`id` INTEGER AUTO_INCREMENT NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `number` INTEGER NOT NULL,
    `city` VARCHAR(34) NOT NULL,
    `province` VARCHAR(2) NOT NULL,
    `cap` VARCHAR(5) NOT NULL,
    
    PRIMARY KEY(`id`)
);

CREATE TABLE `registered_user` (
	`email` VARCHAR(254) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    `surname` VARCHAR(25) NOT NULL,
    `gender` ENUM('M', 'F', 'N') NOT NULL,
    `birthdate` DATE NOT NULL,
    `city_birthplace` VARCHAR(34) NOT NULL,
    `nation_birthplace` VARCHAR(56) NOT NULL,
    `nationality` VARCHAR(56) NOT NULL,
    `profession` VARCHAR(25),
    `num_cellphone` VARCHAR(10),
    `password` VARCHAR(128) NOT NULL,
    `salt_hex` VARCHAR(32) NOT NULL,
    `id_residential_address` INTEGER NOT NULL, 
    
    PRIMARY KEY(`email`),
    
    CONSTRAINT `fk_registereduser_residentialaddress` FOREIGN KEY (`id_residential_address`) 
		REFERENCES `residential_address` (`id`) 
			ON DELETE NO ACTION
			ON UPDATE NO ACTION
);

CREATE TABLE `q_system` (
	`id` INTEGER AUTO_INCREMENT NOT NULL,
    `name` VARCHAR(34) NOT NULL,
    `email_registered_user` VARCHAR(254) NOT NULL,
    
    PRIMARY KEY(`id`), 
    
	CONSTRAINT `fk_qsystem_registereduser` FOREIGN KEY (`email_registered_user`) 
		REFERENCES `registered_user` (`email`)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE `analysis` (
	`id` INTEGER AUTO_INCREMENT NOT NULL,
    `name_transpilation` ENUM("original", "simple", "ibm_perth", "ibm_sherbroke", "rpcx"),
    `optimization` INTEGER NOT NULL,
    `save_date` DATETIME NOT NULL,
    `id_q_system` INTEGER NOT NULL,
    PRIMARY KEY(`id`),
    
	CONSTRAINT `fk_analysis_qsystem` FOREIGN KEY (`id_q_system`) 
		REFERENCES `q_system` (`id`)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE `source_file` (
	`id` INTEGER AUTO_INCREMENT NOT NULL,
    `path` VARCHAR(250) NOT NULL,
    `file` BLOB NOT NULL,
    
    PRIMARY KEY(`id`)
);

CREATE TABLE `result` (
	`id` INTEGER AUTO_INCREMENT NOT NULL, 
    `result_static_analysis` VARCHAR(500) NOT NULL,
    `id_analysis` INTEGER NOT NULL, 
    `id_source_file` INTEGER NOT NULL, 
    
    PRIMARY KEY(`id`), 
    
	CONSTRAINT `fk_result_analysis` FOREIGN KEY (`id_analysis`) 
		REFERENCES `analysis` (`id`)
			ON DELETE CASCADE
            ON UPDATE CASCADE, 
	CONSTRAINT `fk_result_sourcefile` FOREIGN KEY (`id_source_file`) 
		REFERENCES `source_file` (`id`)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE `result_dynamic_analysis` (
	`id` INTEGER AUTO_INCREMENT NOT NULL, 
    `name_q_circuit` VARCHAR(25) NOT NULL, 
    `number_q_circuit` INTEGER NOT NULL, 
    `matrix` VARCHAR(1000) NOT NULL, 
    `result` VARCHAR(500) NOT NULL, 
    `id_result` INTEGER NOT NULL, 
    
    PRIMARY KEY(`id`), 
    
	CONSTRAINT `fk_resultdynamicanalysis_result` FOREIGN KEY (`id_result`) 
		REFERENCES `result` (`id`)
			ON DELETE CASCADE
            ON UPDATE CASCADE
);









