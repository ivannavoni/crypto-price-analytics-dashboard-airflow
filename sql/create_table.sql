-- Create main table for cryptocurrency prices
CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    price DECIMAL(16, 4) NOT NULL,
    time TIMESTAMP NOT NULL,
    CONSTRAINT unique_symbol_time UNIQUE (symbol, time)
);

-- Index for faster queries by symbol and time
CREATE INDEX IF NOT EXISTS idx_crypto_date ON crypto_prices(symbol, time);