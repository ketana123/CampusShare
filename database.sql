-- =====================================================================
-- CampusShare — database.sql
--
-- This script creates the MySQL database and user for CampusShare.
-- The actual TABLES are created automatically by SQLAlchemy the first
-- time the Flask app runs (via db.create_all() in run.py / seed.py), so
-- you do NOT need to write CREATE TABLE statements by hand.
--
-- Usage:
--   mysql -u root -p < database.sql
-- =====================================================================

CREATE DATABASE IF NOT EXISTS campusshare
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Create a dedicated application user (replace the password!)
CREATE USER IF NOT EXISTS 'campusshare_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON campusshare.* TO 'campusshare_user'@'localhost';
FLUSH PRIVILEGES;

-- After running this script, set DATABASE_URL in your .env file to:
--   mysql+pymysql://campusshare_user:change_this_password@localhost/campusshare
--
-- Then run:
--   python run.py       (creates all tables)
--   python seed.py       (inserts demo data)

-- =====================================================================
-- Reference: the tables SQLAlchemy will create (for documentation only)
-- =====================================================================
-- users               (id, full_name, email, password_hash, phone, student_id,
--                       department, year, semester, role, is_blocked,
--                       created_at, updated_at)
-- categories          (id, name, icon, created_at)
-- items               (id, owner_id, category_id, title, description,
--                       listing_type, condition, price, rental_price_per_day,
--                       security_deposit, exchange_for, quantity,
--                       pickup_location, status, is_deleted,
--                       created_at, updated_at)
-- item_images         (id, item_id, filename, created_at)
-- rental_requests     (id, item_id, requester_id, request_type, status,
--                       message, exchange_offer, created_at, updated_at)
-- rentals             (id, request_id, stage, picked_up_at,
--                       return_requested_at, returned_at,
--                       created_at, updated_at)
-- favorites           (id, user_id, item_id, created_at)
-- reviews             (id, reviewer_id, reviewee_id, item_id, request_id,
--                       rating, comment, created_at)
-- notifications       (id, user_id, title, message, link, is_read, created_at)
-- reports             (id, reporter_id, item_id, reported_user_id, reason,
--                       description, status, admin_response,
--                       created_at, updated_at)
