-- Initialize database schema for FastAPI Boilerplate
-- This is a generic schema that can be customized for your specific needs

-- Create a basic example table
CREATE TABLE IF NOT EXISTS example_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_example_data_name ON example_data(name);
CREATE INDEX IF NOT EXISTS idx_example_data_created_at ON example_data(created_at);

-- Insert sample data
INSERT INTO example_data (name, description) VALUES
('Sample Item 1', 'This is a sample item for testing'),
('Sample Item 2', 'Another sample item for demonstration'),
('Sample Item 3', 'Third sample item for reference')
ON CONFLICT (id) DO NOTHING;

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_example_data_updated_at
    BEFORE UPDATE ON example_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();