-- Create a stored procedure named 'AddBonus' to add a new correction for a student
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$

CREATE PROCEDURE AddBonus(
    IN p_user_id INT, 
    IN p_project_name VARCHAR(255), 
    IN p_score FLOAT
)
BEGIN
    DECLARE v_project_id INT;

    -- Check and insert the project if it doesn't exist
    INSERT IGNORE INTO projects (name) VALUES (p_project_name);

    -- Retrieve the project ID
    SET v_project_id = (SELECT id FROM projects WHERE name = p_project_name LIMIT 1);

    -- Insert the correction
    INSERT INTO corrections (user_id, project_id, score) VALUES (p_user_id, v_project_id, p_score);
END$$

DELIMITER ;

