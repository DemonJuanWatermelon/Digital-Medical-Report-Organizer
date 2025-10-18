-- Initialize the medical reports database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create additional indexes for better performance
CREATE INDEX IF NOT EXISTS idx_medical_reports_user_id ON medical_reports(user_id);
CREATE INDEX IF NOT EXISTS idx_medical_reports_created_at ON medical_reports(created_at);
CREATE INDEX IF NOT EXISTS idx_medical_reports_file_type ON medical_reports(file_type);

-- Create full-text search index for OCR text
CREATE INDEX IF NOT EXISTS idx_medical_reports_ocr_text_gin ON medical_reports USING gin(to_tsvector('english', ocr_text));

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create trigger for medical_reports table
CREATE TRIGGER update_medical_reports_updated_at BEFORE UPDATE ON medical_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data (optional)
INSERT INTO users (email, hashed_password, full_name, is_active) VALUES
('admin@medicalorganizer.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2', 'Admin User', true),
('doctor@medicalorganizer.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.5K2', 'Dr. Smith', true)
ON CONFLICT (email) DO NOTHING;
