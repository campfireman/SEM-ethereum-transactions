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

-- empty blocks
SELECT
    COUNT(*)
FROM
    blocks
WHERE
    CAST(gas_used AS DECIMAL) / gas_limit = 0
    AND transaction_count = 0;

-- total value of transactions
CREATE MATERIALIZED VIEW IF NOT EXISTS total_value AS
SELECT
    (SUM(gas) * SUM(gas_price) + SUM(value)) / POWER(10, 18) AS total
FROM
    transactions;

-- ratio of top recievers
SELECT
    t.total / tx.total
FROM
    (
        SELECT
            SUM(total) AS total
        FROM
            top_recievers
    ) AS t,
    total_value AS tx;

-- examine the value of top reciever
SELECT
    t.total / tx.total
FROM
    (
        SELECT
            *
        FROM
            top_recievers
        LIMIT
            1
    ) AS t,
    (
        SELECT
            *
        FROM
            total_value
    ) AS tx;

-- no. of blocks
CREATE MATERIALIZED VIEW IF NOT EXISTS total_no_tx AS
SELECT
    COUNT(*) AS to_no_tx
FROM
    transactions;

-- compare top recievers to total value of transactions
SELECT
    t1.total_top / t2.total AS ratio_of_top
FROM
    (
        SELECT
            SUM(total) AS total_top
        FROM
            top_recievers
    ) AS t1,
    (
        SELECT
            total
        FROM
            total_value
    ) AS t2;

-- examine the transaction volume of top accounts
SELECT
    tx.no_of_tx / CAST(t.total_no_tx AS FLOAT) AS ratio
FROM
    (
        SELECT
            to_address,
            COUNT(*) AS no_of_tx
        FROM
            transactions
        GROUP BY
            to_address
        ORDER BY
            no_of_tx DESC
        LIMIT
            100
    ) AS tx,
    total_no_tx AS t;

SELECT
    SUM(ratio)
FROM
    (
        SELECT
            tx.no_of_tx / CAST(t.total_no_tx AS FLOAT) AS ratio
        FROM
            (
                SELECT
                    t.to_address,
                    COUNT(*) AS no_of_tx
                FROM
                    transactions AS tx
                    RIGHT JOIN top_recievers AS t ON tx.to_address = t.to_address
                GROUP BY
                    t.to_address
                ORDER BY
                    no_of_tx DESC
            ) AS tx,
            total_no_tx AS t
    ) AS t;

\ copy (
    SELECT
        COUNT(*) AS no_of_tx,
        to_address
    FROM
        transactions
    GROUP BY
        to_address
    ORDER BY
        no_of_tx
) TO '/home/ture/studium/19-20SS/SEM/data/no_of_tx.csv' With CSV DELIMITER ',' HEADER;

SELECT
    percentile_cont(0.25) within GROUP (
        ORDER BY
            t.total ASC
    ) AS percentile_25,
    percentile_cont(0.50) within GROUP (
        ORDER BY
            t.total ASC
    ) AS percentile_50,
    percentile_cont(0.75) within GROUP (
        ORDER BY
            t.total ASC
    ) AS percentile_75,
    percentile_cont(0.95) within GROUP (
        ORDER BY
            t.total ASC
    ) AS percentile_95
FROM
    (
        SELECT
            (gas * gas_price + value) / POWER(10, 18) AS total
        FROM
            transactions
    ) AS t;

SELECT
    *
FROM
    blocks
LIMIT
    10;