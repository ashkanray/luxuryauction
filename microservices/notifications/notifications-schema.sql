-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  UNIQUE(username),
  password VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  api_key VARCHAR(100) NOT NULL,
  admin_account BOOLEAN,
  suspended BOOLEAN
);

-- Create all feedback table
CREATE TABLE IF NOT EXISTS feedback (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  email_subject VARCHAR(255) NOT NULL,
  email_body TEXT NOT NULL,
  received TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)