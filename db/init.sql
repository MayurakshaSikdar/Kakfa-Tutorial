CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id INTEGER,
    amount DECIMAL,
    timestamp TEXT,
    is_fraud BOOLEAN,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);