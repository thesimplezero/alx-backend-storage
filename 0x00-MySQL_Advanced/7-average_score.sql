-- Create a stored procedure named 'ComputeAverageScoreForUser' to compute and store the average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    -- Compute the average score and update the users table
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE user_id = p_user_id
    )
    WHERE id = p_user_id;
END$$

DELIMITER ;

