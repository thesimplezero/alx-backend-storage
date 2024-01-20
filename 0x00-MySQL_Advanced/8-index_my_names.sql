-- 1. Select the 'holberton' database for subsequent operations
USE holberton;

-- 2. Introduce a calculated column 'first_letter' to efficiently store the first letter of each name
ALTER TABLE names ADD COLUMN first_letter CHAR(1) GENERATED ALWAYS AS (LEFT(name, 1)) STORED;

-- 3. Create an index 'idx_name_first' on the 'first_letter' column to accelerate queries
-- that filter or sort based on the first letter of names
CREATE INDEX idx_name_first ON names (first_letter);

-- 4. Optimize the 'names' table for improved performance by defragmenting data and reclaiming unused space
OPTIMIZE TABLE names;
