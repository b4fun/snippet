CREATE TABLE `product` (
    `id` int(11) NOT NULL,
    `sku` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `attributes` mediumtext COLLATE utf8mb4_unicode_ci,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `product`
    (`id`, `sku`, `attributes`)
VALUES
    (1, 'pillow-001', '{"color": "red", "size": "lg"}'),
    (2, 'pillow-002', '{"color": "yellow", "size": "lg"}'),
    (3, 'pillow-003', '{"color": "yellow", "size": "sm"}');
