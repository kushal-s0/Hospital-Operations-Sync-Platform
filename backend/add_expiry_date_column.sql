-- Add expiry_date and unit_price columns to inventory_items table

USE hospital_management;

-- Add unit_price column (if not exists)
ALTER TABLE inventory_items
ADD COLUMN IF NOT EXISTS unit_price DECIMAL(10,2) NULL AFTER supplier;

-- Add expiry_date column (if not exists)
ALTER TABLE inventory_items
ADD COLUMN IF NOT EXISTS expiry_date DATE NULL AFTER unit_price;

-- Verify the changes
DESCRIBE inventory_items;

-- Optional: Update some sample data with expiry dates for testing
UPDATE inventory_items SET expiry_date = '2026-12-31', unit_price = 5.50 WHERE category = 'Medicine' AND expiry_date IS NULL LIMIT 3;
UPDATE inventory_items SET expiry_date = '2027-06-30', unit_price = 15.00 WHERE category = 'Consumable' AND expiry_date IS NULL LIMIT 3;
UPDATE inventory_items SET unit_price = 250.00 WHERE category = 'Equipment' AND unit_price IS NULL LIMIT 2;

SELECT 'Columns added successfully!' AS status;
SELECT * FROM inventory_items LIMIT 5;
