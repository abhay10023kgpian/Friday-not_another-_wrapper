INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Air Zoom Pegasus 41', 'n-a-10ab11', 'Nike', 135.00, 'Black/White', '10'),
('React Infinity Run 4', 'n-r-11cd12', 'Nike', 160.00, 'Triple White', '9.5'),
('Zoom Fly 6', 'n-z-12ef13', 'Nike', 170.00, 'Volt/Black', '11'),
('Vaporfly Next 3', 'n-v-13gh14', 'Nike', 215.00, 'University Red', '10.5'),
('Invincible Run 3', 'n-i-14ij15', 'Nike', 180.00, 'Wolf Grey', '9'),
('Structure 25', 'n-s-15kl16', 'Nike', 140.00, 'Obsidian/White', '12'),
('Dunk Low Retro', 'n-d-16mn17', 'Nike', 115.00, 'Panda Black/White', '8.5'),
('Blazer Mid 77 Vintage', 'n-b-17op18', 'Nike', 105.00, 'Sail/Light Bone', '8'),
('Cortez Textile', 'n-c-18qr19', 'Nike', 90.00, 'Forrest Red/White', '7.5'),
('Killshot 2 Leather', 'n-k-19st20', 'Nike', 95.00, 'Midnight Navy/Gum', '10'),
('LeBron XXI Witness', 'n-l-20uv21', 'Nike', 200.00, 'Metallic Gold/Black', '13'),
('Precision 7', 'n-p-21wx22', 'Nike', 75.00, 'Cool Grey/Volt', '11.5'),
('G.T. Cut Academy', 'n-g-22yz23', 'Nike', 95.00, 'Bred/University Red', '12.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Metcon 9 Training', 'n-m-23ab24', 'Nike', 150.00, 'Anthracite/Black', '10'),
('Free Metcon 5', 'n-f-24cd25', 'Nike', 120.00, 'Arctic Orange', '7'),
('Motiva Walking', 'n-m-25ef26', 'Nike', 110.00, 'Photon Dust', '8.5'),
('Promina Comfort', 'n-p-26gh27', 'Nike', 65.00, 'Pure Platinum', '9'),
('Kids Star Runner 4', 'n-k-27ij28', 'Nike', 52.00, 'Game Royal/White', '3'),
('Kids Flex Runner 3', 'n-k-28kl29', 'Nike', 48.00, 'Pink Foam/White', '2'),
('Victori One Slide', 'n-v-29mn30', 'Nike', 35.00, 'Triple Black', '11'),
('Adizero Boston 12', 'a-a-30op31', 'Adidas', 160.00, 'Solar Red/Core Black', '9.5'),
('Adizero Adios Pro 3', 'a-a-31qr32', 'Adidas', 218.00, 'Lucid Lemon', '10'),
('Supernova Rise', 'a-s-32st33', 'Adidas', 140.00, 'Wonder Blue/Silver', '10.5'),
('Solarglide 6', 'a-s-33uv34', 'Adidas', 135.00, 'Core Black/Carbon', '11'),
('Adistar CS 2', 'a-a-34wx35', 'Adidas', 155.00, 'Cloud White/Dash Grey', '8.5'),
('Duramo Speed', 'a-d-35yz36', 'Adidas', 85.00, 'Lucid Cyan', '9')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Samba OG', 'a-s-36ab37', 'Adidas', 100.00, 'Cloud White/Core Black', '8'),
('Superstar XLG', 'a-s-37cd38', 'Adidas', 110.00, 'Core Black/Footwear White', '9.5'),
('NMD R1 V3', 'a-n-38ef39', 'Adidas', 160.00, 'Grey Four/Solar Orange', '10.5'),
('Campus 00s', 'a-c-39gh40', 'Adidas', 110.00, 'Dark Green/Cloud White', '7.5'),
('Forum Low CL', 'a-f-40ij41', 'Adidas', 100.00, 'Chalk White/Crew Navy', '9'),
('Harden Volume 8', 'a-h-41kl42', 'Adidas', 160.00, 'Luxury Green/Black', '13.5'),
('Trae Young 3', 'a-t-42mn43', 'Adidas', 140.00, 'Semi Solar Slime', '12'),
('Dame 8 Extply', 'a-d-43op44', 'Adidas', 130.00, 'Royal Blue/Gold Metallic', '11.5'),
('Dropset 2 Trainer', 'a-d-44qr45', 'Adidas', 130.00, 'Olive Strata/Earth', '10'),
('Amplimove Training', 'a-a-45st46', 'Adidas', 70.00, 'Halo Silver/Black', '8'),
('Cloudfoam Pure 2.0', 'a-c-46uv47', 'Adidas', 75.00, 'Bliss Pink/Core Black', '6.5'),
('Lite Racer Adapt 6.0', 'a-l-47wx48', 'Adidas', 68.00, 'Legend Ink/White', '11'),
('Kids Grand Court 2.0', 'a-k-48yz49', 'Adidas', 46.00, 'Cloud White/Iridescent', '1.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Kids Runfalcon 3.0', 'a-k-49ab50', 'Adidas', 42.00, 'Scarlet/Core Black', '4'),
('Adilette Comfort Slide', 'a-a-50cd51', 'Adidas', 40.00, 'Core Black/Cloud White', '10'),
('Adilette 22 Slide', 'a-a-51ef52', 'Adidas', 55.00, 'Magic Lime', '9'),
('Deviate Nitro 3', 'p-d-52gh53', 'Puma', 160.00, 'Sun Stream/Sunset Glow', '10'),
('Velocity Nitro 3', 'p-v-53ij54', 'Puma', 130.00, 'Psychedelic Rush', '9.5'),
('Magnify Nitro 2', 'p-m-54kl55', 'Puma', 140.00, 'Fast Yellow/Black', '11'),
('ForeverRun Nitro', 'p-f-55mn56', 'Puma', 150.00, 'Electric Peppermint', '10.5'),
('Electrify Nitro 3', 'p-e-56op57', 'Puma', 100.00, 'Ultra Blue/Fire Orchid', '8.5'),
('Speedcat OG', 'p-s-57qr58', 'Puma', 100.00, 'For All Time Red/White', '9'),
('Palermo Leather', 'p-p-58st59', 'Puma', 90.00, 'Cobalt Glaze/Warm White', '8'),
('Cali Court Leather', 'p-c-59uv60', 'Puma', 85.00, 'Alpine Snow/Silver', '7'),
('Future Rider Play On', 'p-f-60wx61', 'Puma', 88.00, 'Dazzling Blue/Green', '10'),
('Mayze Stack Casual', 'p-m-61yz62', 'Puma', 95.00, 'Pristine/Warm Earth', '6.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('MB.03 Melo Toxic', 'p-m-62ab63', 'Puma', 125.00, 'Purple Glimmer/Green', '12'),
('All-Pro Nitro', 'p-a-63cd64', 'Puma', 130.00, 'Lime Squeeze/White', '11.5'),
('Stewie 2 Basketball', 'p-s-64ef65', 'Puma', 120.00, 'Ruby Shimmer', '9.5'),
('PWRFrame TR 3', 'p-p-65gh66', 'Puma', 105.00, 'Puma Black/Strong Grey', '10'),
('Fuse 3.0 Training', 'p-f-66ij67', 'Puma', 120.00, 'Yellow Sizzle/Black', '11'),
('Softride Enzo Evo', 'p-s-67kl68', 'Puma', 68.00, 'Peacoat/High Risk Red', '9'),
('Prowl Slip-On', 'p-p-68mn69', 'Puma', 62.00, 'Rose Quartz/Silver', '7.5'),
('Kids Smash 3.0', 'p-k-69op70', 'Puma', 45.00, 'White/Peacoat/Red', '2.5'),
('Kids Anzarun Lite', 'p-k-70qr71', 'Puma', 40.00, 'Blossom Pink/White', '3'),
('Leadcat 2.0 Slide', 'p-l-71st72', 'Puma', 36.00, 'Navy/White', '10'),
('FuelCell Rebel v4', 'n-f-72uv73', 'New Balance', 140.00, 'Cyberjad/Black', '9.5'),
('FuelCell SuperComp Elite v4', 'n-f-73wx74', 'New Balance', 220.00, 'Neo Flame/White', '10'),
('Fresh Foam X More v4', 'n-f-74yz75', 'New Balance', 150.00, 'Copper Metallic', '11')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Fresh Foam X 880v14', 'n-f-75ab76', 'New Balance', 140.00, 'Marine Blue/Lime', '10.5'),
('Fresh Foam X 860v13', 'n-f-76cd77', 'New Balance', 135.00, 'Arctic Grey/Silver', '9'),
('Fresh Foam Arishi v4', 'n-f-77ef78', 'New Balance', 75.00, 'Phantom/Magnet', '8.5'),
('990v6 Made in USA', 'n-9-78gh79', 'New Balance', 200.00, 'Castlerock/Moonbeam', '10'),
('2002R Protection Pack', 'n-2-79ij80', 'New Balance', 145.00, 'Rain Cloud/Mirage Grey', '9.5'),
('550 Retro Basketball', 'n-5-80kl81', 'New Balance', 110.00, 'Sea Salt/Varsity Green', '8'),
('327 Heritage', 'n-3-81mn82', 'New Balance', 100.00, 'Moonbeam/Classic Burgundy', '7.5'),
('9060 Futuristic', 'n-9-82op83', 'New Balance', 150.00, 'Mushroom/Aluminum', '11'),
('TWO WXY v4', 'n-t-83qr84', 'New Balance', 120.00, 'Electric Red/Gold', '12.5'),
('Kawhi 3 Alpha', 'n-k-84st85', 'New Balance', 160.00, 'Black/Ghost Pepper', '13'),
('Minimus TR v2', 'n-m-85uv86', 'New Balance', 120.00, 'Workwear Amber', '10'),
('FuelCell Trainer v2', 'n-f-86wx87', 'New Balance', 110.00, 'Incense/Team Away Grey', '9'),
('840v1 Walking', 'n-8-87yz88', 'New Balance', 135.00, 'Turtledove/Nimbus Cloud', '10.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('928v3 Motion Control', 'n-9-88ab89', 'New Balance', 155.00, 'Bone/Light Khaki', '11.5'),
('Kids 574 Hook and Loop', 'n-k-89cd90', 'New Balance', 55.00, 'Grey/Sky Blue', '2'),
('Kids Fresh Foam Roav', 'n-k-90ef91', 'New Balance', 60.00, 'Bright Cherry/Black', '3.5'),
('200 Adjustable Slide', 'n-2-91gh92', 'New Balance', 38.00, 'Eclipse Navy', '9'),
('Chuck 70 Canvas High', 'c-c-92ij93', 'Converse', 90.00, 'Parchment/Egret', '9'),
('Run Star Hike Platform', 'c-r-93kl94', 'Converse', 110.00, 'Black/White/Gum', '7.5'),
('One Star Pro Suede', 'c-o-94mn95', 'Converse', 75.00, 'Vintage Navy/White', '8.5'),
('Star Player 76', 'c-s-95op96', 'Converse', 80.00, 'Forest Pine/Egret', '10'),
('Run Star Motion CX', 'c-r-96qr97', 'Converse', 120.00, 'Desert Sand/Light Bone', '8'),
('Chuck Taylor All Star Lift', 'c-c-97st98', 'Converse', 75.00, 'Sunrise Pink/White', '6.5'),
('Weapon Ox Retro', 'c-w-98uv99', 'Converse', 120.00, 'Vintage White/Ash Stone', '10.5'),
('Pro Blaze Classic', 'c-p-99wx10', 'Converse', 70.00, 'White/Cyber Grey', '9.5'),
('Chuck 70 Marquis', 'c-c-10yz11', 'Converse', 130.00, 'Dark Moss/Black', '11')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Cruise Low Top', 'c-c-11ab12', 'Converse', 85.00, 'Egret/Algae Coast', '7'),
('All Star BB Trilliant CX', 'c-a-12cd13', 'Converse', 120.00, 'Aero Jam Teal/Purple', '12'),
('All Star BB Shift', 'c-a-13ef14', 'Converse', 115.00, 'solar Orange/White', '11.5'),
('G4 Low Court', 'c-g-14gh15', 'Converse', 110.00, 'Hyper Magenta/Black', '13'),
('All Star Move Comfort', 'c-a-15ij16', 'Converse', 85.00, 'Stone Mauve', '8'),
('Chuck Taylor Lugged 2.0', 'c-c-16kl17', 'Converse', 125.00, 'Oat Milk/Papyrus', '9'),
('CTAS Malden Street', 'c-c-17mn18', 'Converse', 65.00, 'Obsidian Mist/Grey', '10'),
('Kids Chuck Taylor Easy-On', 'c-k-18op19', 'Converse', 45.00, 'Optical White', '1'),
('Kids Pro Blaze Strap', 'c-k-19qr20', 'Converse', 50.00, 'Navy/Red/White', '3'),
('Kids Star Replay', 'c-k-20st21', 'Converse', 42.00, 'Laser Lemon/Black', '2.5'),
('All Star Slide Sandal', 'c-a-21uv22', 'Converse', 35.00, 'Engine Smoke/White', '9'),
('Sk8-Hi Classic', 'v-s-22wx23', 'Vans', 80.00, 'Navy/White Canvas', '9.5'),
('Authentic Canvas', 'v-a-23yz24', 'Vans', 60.00, 'Red/True White', '8.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Classic Slip-On Checkerboard', 'v-c-24ab25', 'Vans', 65.00, 'Black/Off White Check', '9'),
('Knu Skool Suede', 'v-k-25cd26', 'Vans', 75.00, 'Black/True White', '10'),
('Era Core Skate', 'v-e-26ef27', 'Vans', 60.00, 'Pewter/Black', '8'),
('Rowley Classic', 'v-r-27gh28', 'Vans', 85.00, 'Racing Red/Navy', '10.5'),
('Half Cab 33 DX', 'v-h-28ij29', 'Vans', 95.00, 'Taupe/Marsh', '11'),
('Lowland ComfyCush', 'v-l-29kl30', 'Vans', 90.00, 'White/Flame Orange', '7.5'),
('Wayvee Skate', 'v-w-30mn31', 'Vans', 88.00, 'Dusty Olive/Black', '9.5'),
('Zahba Mid', 'v-z-31op32', 'Vans', 92.00, 'Light Khaki/Gum', '10'),
('UltraRange Exo', 'v-u-32qr33', 'Vans', 100.00, 'Port Royale/White', '9'),
('UltraRange Neo VR3', 'v-u-33st34', 'Vans', 125.00, 'Multi/Turtledove', '10.5'),
('Crosspath All-Terrain', 'v-c-34uv35', 'Vans', 130.00, 'Forest Night/Gum', '11'),
('MTE UltraRange Exo Hi', 'v-m-35wx36', 'Vans', 140.00, 'Walnut/Marshmallow', '12'),
('ComfyCush One Walk', 'v-c-36yz37', 'Vans', 72.00, 'Cloud Dancer', '8.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Kids Old Skool V', 'v-k-37ab38', 'Vans', 50.00, 'Black/True White Velcro', '2'),
('Kids Sk8-Mid Reissue V', 'v-k-38cd39', 'Vans', 52.00, 'Golden Glow/White', '3'),
('Kids Slip-On Bunny', 'v-k-39ef40', 'Vans', 48.00, 'Pastel Lilac', '1.5'),
('La Costa Slide-On', 'v-l-40gh41', 'Vans', 38.00, 'Checkerboard Black', '10'),
('Harbor Mule VR3', 'v-h-41ij42', 'Vans', 65.00, 'Sand Shell', '9'),
('Gel-Nimbus 26', 'a-g-42kl43', 'Asics', 160.00, 'Feather Grey/Black', '10'),
('Novablast 4', 'a-n-43mn44', 'Asics', 140.00, 'Illuminate Mint', '9.5'),
('Superblast 2', 'a-s-44op45', 'Asics', 200.00, 'Paris Sunrise Red', '10.5'),
('GT-2000 12', 'a-g-45qr46', 'Asics', 140.00, 'French Blue/White', '11'),
('Gel-Cumulus 26', 'a-g-46st47', 'Asics', 140.00, 'Mint Tint/Pale Mint', '8.5'),
('Metaspeed Sky Paris', 'a-m-47uv48', 'Asics', 219.00, 'Sunrise Red/Black', '9'),
('Noosa Tri 15', 'a-n-48wx49', 'Asics', 130.00, 'Vibrant Yellow/Multi', '10'),
('Gel-Excite 10', 'a-g-49yz50', 'Asics', 85.00, 'Carrier Grey/Neon Lime', '11.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Gel-Venture 9 Trail', 'a-g-50ab51', 'Asics', 80.00, 'Mantle Green/Orange', '12'),
('Gel-Contend 8', 'a-g-51cd52', 'Asics', 70.00, 'Indigo Blue/Silver', '9.5'),
('Magic Speed 3', 'a-m-52ef53', 'Asics', 160.00, 'White/Sea Glass', '10'),
('Gel-Trabuco 12', 'a-g-53gh54', 'Asics', 140.00, 'Obsidian Grey/Java', '10.5'),
('Gel-NYC Lifestyle', 'a-g-54ij55', 'Asics', 130.00, 'Cream/Oyster Grey', '9'),
('Gel-1130 Retro', 'a-g-55kl56', 'Asics', 95.00, 'White/Clay Canyon', '8'),
('Japan S Classic', 'a-j-56mn57', 'Asics', 80.00, 'White/Steeple Grey', '8.5'),
('EX89 Court Heritage', 'a-e-57op58', 'Asics', 110.00, 'White/Midnight Navy', '11'),
('Gel-Quantum 180 VII', 'a-g-58qr59', 'Asics', 130.00, 'Black/Cayenne', '10'),
('Kids Contend 8 PS', 'a-k-59st60', 'Asics', 54.00, 'Digital Aqua/White', '2'),
('Kids Pre-Noosa Tri 15', 'a-k-60uv61', 'Asics', 62.00, 'Island Blue/Sun Peach', '3.5'),
('Actibreeze 3D Sandal', 'a-a-61wx62', 'Asics', 80.00, 'Mako Blue', '10'),
('Floatzig 1 Running', 'r-f-62yz63', 'Reebok', 130.00, 'Vector Blue/Solar Acid', '9.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Floatride Energy 5', 'r-f-63ab64', 'Reebok', 110.00, 'Gable Grey/Dynamic Red', '10'),
('Energen Tech Plus', 'r-e-64cd65', 'Reebok', 65.00, 'Core Black/Pure Grey', '9'),
('Club C 85 Vintage', 'r-c-65ef66', 'Reebok', 90.00, 'Chalk/Glen Green', '8.5'),
('Classic Nylon Retro', 'r-c-66gh67', 'Reebok', 75.00, 'Platinum/Jet Black', '10.5'),
('Club C Revenge', 'r-c-67ij68', 'Reebok', 85.00, 'Ftwr White/Vector Navy', '8'),
('BB 4000 II Low', 'r-b-68kl69', 'Reebok', 90.00, 'White/burgundy/Gum', '9.5'),
('LT Court Leather', 'r-l-69mn70', 'Reebok', 100.00, 'Alabaster/Seaside Grey', '11'),
('Question Mid Iverson', 'r-q-70op71', 'Reebok', 170.00, 'White/Pearlized Red', '12'),
('Shaq Attaq OG', 'r-s-71qr72', 'Reebok', 180.00, 'White/Azure Blue/Black', '14'),
('Pump Omni Zone II', 'r-p-72st73', 'Reebok', 160.00, 'Chalk/Bright Ochre', '11.5'),
('Nano X4 Training', 'r-n-73uv74', 'Reebok', 140.00, 'Black/Amber Gold', '10'),
('Nano X3 Froning', 'r-n-74wx75', 'Reebok', 150.00, 'Vintage Chalk/Olive', '9.5'),
('Nanoflex TR 2.0', 'r-n-75yz76', 'Reebok', 80.00, 'Cold Grey/Cyan', '9')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Lifter PR III', 'r-l-76ab77', 'Reebok', 120.00, 'Black/White/Pewter', '10.5'),
('JJ IV Training', 'r-j-77cd78', 'Reebok', 100.00, 'Collegiate Navy/Silver', '11'),
('Walk Ultra 7 DMX Max', 'r-w-78ef79', 'Reebok', 75.00, 'Black/Alloy Grey', '10'),
('Work N Cushion 4.0', 'r-w-79gh80', 'Reebok', 60.00, 'Clean White/Cold Grey', '9'),
('Kids Classic Leather Step N Flash', 'r-k-80ij81', 'Reebok', 48.00, 'Silver Metallic/Pink', '2'),
('Kids Rush Runner 4', 'r-k-81kl82', 'Reebok', 40.00, 'Vector Red/Black', '4'),
('Bondi 8 Cushioned', 'h-b-82mn83', 'Hoka', 165.00, 'Sharkskin/Harbor Mist', '10'),
('Arahi 7 Stability', 'h-a-83op84', 'Hoka', 145.00, 'Frost/Gold Fusion', '9.5'),
('Speedgoat 6 Trail', 'h-s-84qr85', 'Hoka', 155.00, 'Galactic Grey/Hoka Blue', '10.5'),
('Mach 6 Speed', 'h-m-85st86', 'Hoka', 140.00, 'Poppy/Squash', '9'),
('Rincon 4 Lightweight', 'h-r-86uv87', 'Hoka', 125.00, 'Skyward Blue/White', '8.5'),
('Gaviota 5 Max Support', 'h-g-87wx88', 'Hoka', 175.00, 'Harbor Mist/Pebble', '11'),
('Challenger 7 All-Terrain', 'h-c-88yz89', 'Hoka', 145.00, 'Dune/Oxford Tan', '10')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Cielo X1 Carbon', 'h-c-89ab90', 'Hoka', 219.00, 'Evening Sky/Lettuce', '9.5'),
('Rocket X 2 Marathon', 'h-r-90cd91', 'Hoka', 215.00, 'Solar Flare/Black', '10'),
('Skyflow Daily Runner', 'h-s-91ef92', 'Hoka', 160.00, 'Midnight/Electric Cobalt', '11.5'),
('Kawana 2 Gym', 'h-k-92gh93', 'Hoka', 140.00, 'Blanc De Blanc/Silver', '8'),
('Solimar Cross Trainer', 'h-s-93ij94', 'Hoka', 125.00, 'Outer Space/White', '9'),
('Transport Commuter', 'h-t-94kl95', 'Hoka', 150.00, 'Eggnog/Shifting Sand', '10'),
('Clifton L Suede', 'h-c-95mn96', 'Hoka', 170.00, 'Cosmic Grey/Chalk', '9.5'),
('Bondi SR Slip-Resistant', 'h-b-96op97', 'Hoka', 175.00, 'Triple Black Leather', '12'),
('Anacapa 2 Low GTX', 'h-a-97qr98', 'Hoka', 170.00, 'Oak/Alabaster', '10.5'),
('Restore TC Slip-On', 'h-r-98st99', 'Hoka', 110.00, 'Dark Olive/Black', '9'),
('Kids Clifton 9', 'h-k-99uv10', 'Hoka', 110.00, 'Scuba Blue/Clementine', '3.5'),
('Kids Speedgoat 5 Youth', 'h-k-10wx11', 'Hoka', 115.00, 'Fuchsia/Solar', '4'),
('Ora Recovery Slide 3', 'h-o-11yz12', 'Hoka', 60.00, 'Aero Green', '10')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('Infinite Elite Running', 'u-i-12ab13', 'Under Armour', 160.00, 'Lime Surge/Black', '10'),
('Velociti Pro Carbon', 'u-v-13cd14', 'Under Armour', 155.00, 'White/Beta Red', '9.5'),
('HOVR Sonic 6', 'u-h-14ef15', 'Under Armour', 110.00, 'Mod Grey/Jet Grey', '10.5'),
('HOVR Machina 3', 'u-h-15gh16', 'Under Armour', 150.00, 'Breeze/High-Vis Yellow', '11'),
('Charged Assert 10', 'u-c-16ij17', 'Under Armour', 75.00, 'Academy Navy/White', '9'),
('Surge 4 Running', 'u-s-17kl18', 'Under Armour', 65.00, 'Pitch Grey/Red', '8.5'),
('Pegasus Trail 5', 'u-p-18mn19', 'Under Armour', 130.00, 'Baroque Brown/Orange', '12'),
('Forge 96 Lifestyle', 'u-f-19op20', 'Under Armour', 115.00, 'Sandstone/Black', '9.5'),
('SlipSpeed Mega', 'u-s-20qr21', 'Under Armour', 160.00, 'Metallic Silver/Cyan', '10'),
('Curry 11 Future', 'u-c-21st22', 'Under Armour', 160.00, 'Dub Nation Royal/Gold', '11.5'),
('Curry Splash 24', 'u-c-22uv23', 'Under Armour', 110.00, 'Taxi Yellow/Black', '12.5'),
('Spawn 6 Basketball', 'u-s-23wx24', 'Under Armour', 115.00, 'Carolina Blue/White', '13'),
('Project Rock 6', 'u-p-24yz25', 'Under Armour', 160.00, 'Blood Orange/Black', '10.5')
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO products (product_name, product_id, brand_name, price, color, size) VALUES
('TriBase Reign 6', 'u-t-25ab26', 'Under Armour', 140.00, 'Castlerock/White', '10'),
('Commit TR 4', 'u-c-26cd27', 'Under Armour', 85.00, 'Midnight Navy/Gold', '9'),
('Apparition Retro Walk', 'u-a-27ef28', 'Under Armour', 110.00, 'Summit White/Grey', '8.5'),
('Charged Rogue 4', 'u-c-28gh29', 'Under Armour', 80.00, 'Gravel/Neon Coral', '7.5'),
('Kids Assert 10 AC', 'u-k-29ij30', 'Under Armour', 55.00, 'Electric Blue/Lime', '2.5'),
('Kids Scramjet 5', 'u-k-30kl31', 'Under Armour', 58.00, 'Cerise Pink/Purple', '3'),
('Ignite Pro Slide', 'u-i-31mn32', 'Under Armour', 40.00, 'White/Metallic Gold', '11')
ON CONFLICT (product_id) DO NOTHING;