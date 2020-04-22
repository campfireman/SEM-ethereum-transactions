CREATE TABLE transactions (
    id SERIAL PRIMARY KEY NOT NULL,
    hash VARCHAR(66) NOT NULL,
    nonce BIGINT NOT NULL,
    block_hash VARCHAR(66) NOT NULL,
    block_number BIGINT NOT NULL,
    transaction_index BIGINT NOT NULL,
    from_address VARCHAR(66) NOT NULL,
    to_address VARCHAR(66),
    value NUMERIC NOT NULL,
    gas NUMERIC NOT NULL,
    gas_price NUMERIC NOT NULL,
    input TEXT NOT NULL,
    block_timestamp INT NOT NULL
);

COPY transactions (
    hash,
    nonce,
    block_hash,
    block_number,
    transaction_index,
    from_address,
    to_address,
    value,
    gas,
    gas_price,
    input,
    block_timestamp
)
FROM
    '/home/ture/studium/19-20SS/data/transactions.csv' CSV DELIMITER ',' HEADER;

CREATE TABLE blocks (
    id SERIAL NOT NULL,
    number BIGINT NOT NULL,
    hash VARCHAR(66) NOT NULL,
    parent_hash VARCHAR(66) NOT NULL,
    nonce VARCHAR(66) NOT NULL,
    sha3_uncles VARCHAR(66) NOT NULL,
    logs_bloom TEXT NOT NULL,
    transactions_root VARCHAR(66) NOT NULL,
    state_root VARCHAR(66) NOT NULL,
    receipts_root VARCHAR(66) NOT NULL,
    miner VARCHAR(66) NOT NULL,
    difficulty BIGINT NOT NULL,
    total_difficulty NUMERIC NOT NULL,
    size INTEGER NOT NULL,
    extra_data TEXT NOT NULL,
    gas_limit BIGINT NOT NULL,
    gas_used BIGINT NOT NULL,
    timestamp INTEGER,
    transaction_count INTEGER
);

COPY blocks (
    number,
    hash,
    parent_hash,
    nonce,
    sha3_uncles,
    logs_bloom,
    transactions_root,
    state_root,
    receipts_root,
    miner,
    difficulty,
    total_difficulty,
    size,
    extra_data,
    gas_limit,
    gas_used,
    timestamp,
    transaction_count
)
FROM
    '/home/ture/studium/19-20SS/data/blocks.csv' CSV DELIMITER ',' HEADER;

----
CREATE MATERIALIZED VIEW IF NOT EXISTS top_recievers AS
SELECT
    to_address,
    (SUM(gas) * SUM(gas_price) + SUM(value)) / POWER(10, 18) AS total
FROM
    transactions
WHERE
    to_address IS NOT NULL
GROUP BY
    to_address
ORDER BY
    total DESC
LIMIT
    100;

SELECT
    *
FROM
    top_recievers;

CREATE MATERIALIZED VIEW IF NOT EXISTS top_calcers AS
SELECT
    to_address,
    (SUM(gas) * SUM(gas_price)) / POWER(10, 18) AS total
FROM
    transactions
WHERE
    to_address IS NOT NULL
GROUP BY
    to_address
ORDER BY
    total DESC
LIMIT
    100;

SELECT
    *
FROM
    top_calcers;

CREATE MATERIALIZED VIEW IF NOT EXISTS top_valuers AS
SELECT
    to_address,
    SUM(value) / POWER(10, 18) AS total
FROM
    transactions
WHERE
    to_address IS NOT NULL
GROUP BY
    to_address
ORDER BY
    total DESC
LIMIT
    100;

SELECT
    *
FROM
    top_valuers;

-- no. of blocks
SELECT
    COUNT(*)
FROM
    blocks;

-- empty blocks
SELECT
    COUNT(*)
FROM
    blocks
WHERE
    CAST(gas_used AS DECIMAL) / gas_limit = 0
    AND transaction_count = 0;