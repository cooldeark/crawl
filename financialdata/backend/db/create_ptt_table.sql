-- 创建名为 ptt_data 的数据库
CREATE DATABASE IF NOT EXISTS ptt_data;

-- 选择 ptt_data 数据库 (如果只有一個要新增，可以這樣寫，一開始就先定義好)
-- USE ptt_data;

-- 在 ptt_data 数据库中创建一个示例表，例如名为 posts 的表
-- CREATE TABLE IF NOT EXISTS posts (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     author VARCHAR(255) NOT NULL,
--     date_posted DATE,
--     content TEXT,
--     url VARCHAR(255)
-- );

-- 不過還是這個萬用，可以在同一個sql檔案裡面針對不同的database作增加
CREATE TABLE `ptt_data`.`mobiles`(
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `CreateTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- `TradeVolume` BIGINT NOT NULL,
    -- `Transaction` INT NOT NULL,
    -- `TradeValue` BIGINT NOT NULL,
    -- `Open` FLOAT NOT NULL,
    -- `Max` FLOAT NOT NULL,
    -- `Min` FLOAT NOT NULL,
    -- `Close` FLOAT NOT NULL,
    -- `Change` FLOAT NOT NULL,
    -- `Date` DATE NOT NULL,
    -- PRIMARY KEY(`StockID`, `Date`)
);

