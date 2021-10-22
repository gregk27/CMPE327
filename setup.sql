DELETE from USER where 1=1;
DELETE from PRODUCT where 1=1;

INSERT INTO USER (id, username, email, password, balance) VALUES 
('2e649ac0-da77-4021-8257-75d1b85e1610', 'Greg', '18gpk2@queensu.ca', 'b4719d80-aa91-4622-ad5c-292e8516b4b0:4b7914b701ad21fb545b96a8641472cfb2cd4b5e1dc5cbc57df8a8a654a0b57b406f1f12af065a668b836a44dbfe9e038375ac127be4ad44c4e249a7682e9c87', '100.0');
INSERT INTO USER (id, username, email, password, balance) VALUES 
('2e649ac0-da77-4021-8257-75d1b85e1609', 'Greg 2', '18gpk3@queensu.ca', 'b4719d80-aa91-4622-ad5c-292e8516b4b0:4b7914b701ad21fb545b96a8641472cfb2cd4b5e1dc5cbc57df8a8a654a0b57b406f1f12af065a668b836a44dbfe9e038375ac127be4ad44c4e249a7682e9c87', '100.0');
INSERT INTO USER (id, username, email, password, balance) VALUES 
('2e649ac0-da77-4021-8257-75d1b85e1608', 'Greg 3', '18gpk4@queensu.ca', 'b4719d80-aa91-4622-ad5c-292e8516b4b0:4b7914b701ad21fb545b96a8641472cfb2cd4b5e1dc5cbc57df8a8a654a0b57b406f1f12af065a668b836a44dbfe9e038375ac127be4ad44c4e249a7682e9c87', '100.0');

INSERT INTO PRODUCT (id, productName, userId, ownerEmail, price, description, lastModifiedDate) VALUES
('2e649ac0-da77-4021-8257-1234', 'G2 Product', '2e649ac0-da77-4021-8257-75d1b85e1609', '18gpk3@queensu.ca', 500, 'A product owned by Greg 2', CURRENT_TIMESTAMP);
INSERT INTO PRODUCT (id, productName, userId, ownerEmail, price, description, lastModifiedDate) VALUES
('2e649ac0-da77-4021-8257-123456', 'G2 Product 2', '2e649ac0-da77-4021-8257-75d1b85e1609', '18gpk3@queensu.ca', 1000, 'A second product owned by Greg 2', CURRENT_TIMESTAMP);
INSERT INTO PRODUCT (id, productName, userId, ownerEmail, price, description, lastModifiedDate) VALUES
('2e649ac0-da77-4021-8257-13345678', 'G3 Product', '2e649ac0-da77-4021-8257-75d1b85e1608', '18gpk4@queensu.ca', 750, 'A product owned by Greg 3', CURRENT_TIMESTAMP);
INSERT INTO PRODUCT (id, productName, userId, ownerEmail, price, description, lastModifiedDate) VALUES
('2e649ac0-da77-4021-8257-120034', 'G Product', '2e649ac0-da77-4021-8257-75d1b85e1610', '18gpk2@queensu.ca', 500, 'A product owned by Greg', CURRENT_TIMESTAMP);
INSERT INTO PRODUCT (id, productName, userId, ownerEmail, price, description, lastModifiedDate) VALUES
('2e649ac0-da77-4021-8257-100234', 'G Product 2', '2e649ac0-da77-4021-8257-75d1b85e1610', '18gpk2@queensu.ca', 500, 'A second product owned by Greg', CURRENT_TIMESTAMP);

SELECT * from USER;
SELECT product.*, u.username AS username from product INNER JOIN user u WHERE userId==u.id;