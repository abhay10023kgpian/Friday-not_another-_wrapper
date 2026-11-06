
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL UNIQUE,
    brand_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    color VARCHAR(50) NOT NULL,
    size VARCHAR(50) NOT NULL
);

INSERT INTO products (
    product_name, product_id, brand_name, price, color, size
)
VALUES
    ('Air Max 90', 'n-a-01ab12', 'Nike', 130.00, 'White/Black', '10'),
    ('Ultraboost Light', 'a-u-02cd34', 'Adidas', 190.00, 'Core Black', '9'),
    ('Suede Classic XXI', 'p-s-03ef56', 'Puma', 75.00, 'Red/White', '8'),
    ('574 Core', 'n-c-04gh78', 'New Balance', 89.99, 'Grey', '11'),
    ('Chuck Taylor All Star', 'c-t-05ij90', 'Converse', 65.00, 'Optical White', '7'),
    ('Old Skool Classic', 'v-o-06kl12', 'Vans', 70.00, 'Black/White', '6'),
    ('Gel-Kayano 30', 'a-g-07mn34', 'Asics', 160.00, 'Blue/Yellow', '12'),
    ('Classic Leather', 'r-c-08op56', 'Reebok', 85.00, 'Chalk/Gum', '5'),
    ('Clifton 9', 'h-c-09qr78', 'Hoka', 145.00, 'Neon Orange', '9'),
    ('Air Force 1 ''07', 'n-f-10st90', 'Nike', 115.00, 'Triple White', '4'),
    ('Gazelle Indoor', 'a-g-11uv12', 'Adidas', 120.00, 'Collegiate Green', '3'),
    ('Kids Dynamo Free', 'n-d-12wx34', 'Nike', 55.00, 'Crimson', '2'),
    ('Toddler Chuck Taylor', 'c-k-13yz56', 'Converse', 40.00, 'Pink', '1'),
    ('Fresh Foam X 1080v13', 'n-f-14ab78', 'New Balance', 164.99, 'Navy', '10'),
    ('RS-X Efekt', 'p-r-15cd90', 'Puma', 110.00, 'Multi/Black', '8')
ON CONFLICT (product_id) DO NOTHING;
