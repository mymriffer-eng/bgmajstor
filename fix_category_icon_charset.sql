-- Fix MySQL charset/collation for the Category.icon field so emoji icons work.
-- Run this in phpMyAdmin > Databases > SQL or in cPanel MySQL terminal.

ALTER TABLE core_category
  CONVERT TO CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

ALTER TABLE core_category
  MODIFY icon VARCHAR(50)
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

SELECT TABLE_NAME, TABLE_COLLATION
FROM information_schema.TABLES
WHERE TABLE_NAME = 'core_category';
