-- ============================================================
-- GYM MANAGEMENT SYSTEM - DATABASE SETUP SCRIPT
-- Database: MySQL 8.0
-- ============================================================

DROP DATABASE IF EXISTS gym_db;
CREATE DATABASE gym_db;
USE gym_db;

-- ============================================================
-- TABLE CREATION (DDL)
-- ============================================================

CREATE TABLE plans (
    plan_id INT PRIMARY KEY AUTO_INCREMENT,
    plan_name VARCHAR(30) NOT NULL,
    duration_months INT NOT NULL CHECK (duration_months > 0),
    price DECIMAL(8,2) NOT NULL CHECK (price > 0)
);

CREATE TABLE trainers (
    trainer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    specialization VARCHAR(40),
    phone VARCHAR(15) UNIQUE
);

CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE,
    join_date DATE NOT NULL,
    plan_id INT,
    trainer_id INT,
    status ENUM('Active','Expired','Inactive') DEFAULT 'Active',
    FOREIGN KEY (plan_id) REFERENCES plans(plan_id) ON DELETE SET NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id) ON DELETE SET NULL
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    amount DECIMAL(8,2) NOT NULL CHECK (amount > 0),
    payment_date DATE NOT NULL,
    mode ENUM('Cash','UPI','Card') NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

CREATE TABLE attendance (
    att_id INT PRIMARY KEY AUTO_INCREMENT,
    member_id INT NOT NULL,
    check_in DATETIME NOT NULL,
    check_out DATETIME,
    CHECK (check_out IS NULL OR check_out > check_in),
    FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

CREATE TABLE audit_log (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(30) NOT NULL,
    table_name VARCHAR(30) NOT NULL,
    record_id INT,
    description VARCHAR(255),
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- PERFORMANCE INDEXES
-- ============================================================

CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_payments_member ON payments(member_id);
CREATE INDEX idx_attendance_member_date ON attendance(member_id, check_in);
CREATE INDEX idx_audit_action_time ON audit_log(action_type, action_time);
CREATE INDEX idx_members_status ON members(status);
CREATE INDEX idx_members_plan ON members(plan_id);
CREATE INDEX idx_members_trainer ON members(trainer_id);

-- ============================================================
-- VIEW: member_details
-- ============================================================

CREATE VIEW member_details AS
SELECT 
    m.member_id,
    m.name,
    m.phone,
    m.email,
    m.join_date,
    m.status,
    p.plan_name,
    p.price,
    p.duration_months,
    t.name AS trainer_name,
    t.specialization
FROM members m
LEFT JOIN plans p ON m.plan_id = p.plan_id
LEFT JOIN trainers t ON m.trainer_id = t.trainer_id;

-- ============================================================
-- SAMPLE DATA (DML)
-- ============================================================

INSERT INTO plans (plan_name, duration_months, price) VALUES
('Monthly', 1, 1500.00),
('Quarterly', 3, 4000.00),
('Half-Yearly', 6, 7500.00),
('Yearly', 12, 14000.00),
('Annual Plus', 12, 20000.00);

INSERT INTO trainers (name, specialization, phone) VALUES
('Rahul Sharma', 'Weight Training', '9876543210'),
('Priya Deshmukh', 'Yoga', '9823456789'),
('Amit Patel', 'Cardio', '9765432187'),
('Vikram Singh', 'CrossFit', '9812345678'),
('Neha Kulkarni', 'Zumba', '9988776655');

INSERT INTO members (name, phone, email, join_date, plan_id, trainer_id) VALUES
('Dhruv Abhyankar', '9823014576', 'dhruv.abhyankar@gmail.com', '2026-01-10', 2, 1),
('Rohit Verma', '9765432891', 'rohit.verma92@yahoo.com', '2026-02-15', 1, 2),
('Sneha Kulkarni', '9987234510', 'sneha.kulkarni@gmail.com', '2026-03-01', 4, 3),
('Arjun Kale', '9823567412', 'arjun.kale@gmail.com', '2026-03-20', 3, 4),
('Priya Joshi', '9738291056', 'priya.joshi@outlook.com', '2026-04-05', 2, 5),
('Karan Mehta', '9812347650', 'karan.mehta@gmail.com', '2026-04-18', 1, 1),
('Ananya Deshpande', '9923145678', 'ananya.d@gmail.com', '2026-05-02', 4, 2),
('Siddharth Rao', '9765123408', 'sid.rao21@gmail.com', '2026-05-15', 5, 4),
('Riya Patil', '9887654321', 'riya.patil@gmail.com', '2026-06-01', 3, 3),
('Aditya Nair', '9834567123', 'aditya.nair@gmail.com', '2026-06-20', 2, 5);

INSERT INTO payments (member_id, amount, payment_date, mode) VALUES
(1, 4000.00, '2026-01-10', 'UPI'),
(2, 1500.00, '2026-02-15', 'Cash'),
(3, 14000.00, '2026-03-01', 'Card'),
(4, 7500.00, '2026-03-20', 'UPI'),
(5, 4000.00, '2026-04-05', 'Cash'),
(6, 1500.00, '2026-04-18', 'UPI'),
(7, 14000.00, '2026-05-02', 'Card'),
(8, 20000.00, '2026-05-15', 'UPI'),
(9, 7500.00, '2026-06-01', 'Cash'),
(10, 4000.00, '2026-06-20', 'UPI'),
(2, 1500.00, '2026-03-15', 'Cash'),
(4, 7500.00, '2026-06-20', 'UPI'),
(6, 1500.00, '2026-05-18', 'Cash'),
(1, 4000.00, '2026-04-10', 'UPI');

INSERT INTO attendance (member_id, check_in, check_out) VALUES
(1, '2026-09-20 07:00:00', '2026-09-20 08:30:00'),
(1, '2026-09-21 07:15:00', '2026-09-21 08:45:00'),
(1, '2026-09-23 06:50:00', '2026-09-23 08:20:00'),
(2, '2026-09-21 18:00:00', '2026-09-21 19:00:00'),
(2, '2026-09-22 18:30:00', '2026-09-22 19:45:00'),
(3, '2026-09-20 08:30:00', '2026-09-20 10:00:00'),
(3, '2026-09-22 08:15:00', '2026-09-22 09:45:00'),
(4, '2026-09-21 07:30:00', '2026-09-21 08:45:00'),
(4, '2026-09-23 07:45:00', '2026-09-23 09:00:00'),
(5, '2026-09-20 17:00:00', '2026-09-20 18:15:00'),
(5, '2026-09-22 17:30:00', '2026-09-22 18:45:00'),
(6, '2026-09-21 06:45:00', '2026-09-21 08:15:00'),
(6, '2026-09-23 06:55:00', '2026-09-23 08:20:00'),
(7, '2026-09-20 09:00:00', '2026-09-20 10:30:00'),
(8, '2026-09-21 19:00:00', '2026-09-21 20:30:00'),
(8, '2026-09-22 19:15:00', '2026-09-22 20:45:00'),
(9, '2026-09-20 10:30:00', '2026-09-20 12:00:00'),
(9, '2026-09-23 10:45:00', '2026-09-23 12:15:00'),
(10, '2026-09-21 20:00:00', '2026-09-21 21:15:00'),
(10, '2026-09-23 20:15:00', '2026-09-23 21:30:00');

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

DROP PROCEDURE IF EXISTS monthly_revenue;
DELIMITER //
CREATE PROCEDURE monthly_revenue(IN month_year VARCHAR(7))
BEGIN
    SELECT 
        month_year AS period,
        COUNT(*) AS payment_count,
        IFNULL(SUM(amount), 0) AS total_revenue
    FROM payments
    WHERE DATE_FORMAT(payment_date, '%Y-%m') = month_year;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS expire_memberships;
DELIMITER //
CREATE PROCEDURE expire_memberships()
BEGIN
    DECLARE affected INT DEFAULT 0;
    SET SQL_SAFE_UPDATES = 0;
    UPDATE members m
    JOIN plans p ON m.plan_id = p.plan_id
    SET m.status = 'Expired'
    WHERE m.status = 'Active'
      AND DATE_ADD(m.join_date, INTERVAL p.duration_months MONTH) < CURDATE();
    SET affected = ROW_COUNT();
    SET SQL_SAFE_UPDATES = 1;
    INSERT INTO audit_log (action_type, table_name, description)
    VALUES ('PROCEDURE', 'members',
            CONCAT('expire_memberships() marked ', affected, ' member(s) as Expired'));
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS top_members;
DELIMITER //
CREATE PROCEDURE top_members(IN top_n INT)
BEGIN
    SELECT 
        m.member_id,
        m.name,
        COUNT(p.payment_id) AS payment_count,
        SUM(p.amount) AS total_paid
    FROM members m
    JOIN payments p ON m.member_id = p.member_id
    GROUP BY m.member_id, m.name
    ORDER BY total_paid DESC
    LIMIT top_n;
END //
DELIMITER ;

-- ============================================================
-- TRIGGERS
-- ============================================================

DROP TRIGGER IF EXISTS payment_after_insert;
DELIMITER //
CREATE TRIGGER payment_after_insert
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action_type, table_name, record_id, description)
    VALUES ('INSERT', 'payments', NEW.payment_id,
            CONCAT('Payment of Rs.', NEW.amount, ' via ', NEW.mode,
                   ' for member_id ', NEW.member_id));
END //
DELIMITER ;

DROP TRIGGER IF EXISTS member_after_delete;
DELIMITER //
CREATE TRIGGER member_after_delete
AFTER DELETE ON members
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (action_type, table_name, record_id, description)
    VALUES ('DELETE', 'members', OLD.member_id,
            CONCAT('Member "', OLD.name, '" (phone: ', OLD.phone, ') was deleted'));
END //
DELIMITER ;

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

SELECT 'Tables created:' AS status;
SHOW TABLES;

SELECT 'Member count:' AS status, COUNT(*) AS total FROM members;
SELECT 'Payment count:' AS status, COUNT(*) AS total FROM payments;
SELECT 'Attendance count:' AS status, COUNT(*) AS total FROM attendance;

SELECT 'Sample members:' AS status;
SELECT member_id, name, phone, status FROM members;