DROP TABLE IF EXISTS cchangelog;
CREATE TABLE cchangelog (
    id INT NOT NULL AUTO_INCREMENT,
    entity_type VARCHAR(64),
    entity_id INT NOT NULL,
    parent_type VARCHAR(64),
    parent_id INT,
    user_id INT,
    action VARCHAR(64),
    insdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    old_values JSON,
    PRIMARY KEY(id)
);

INSERT INTO cchangelog (entity_type, entity_id, parent_type, parent_id, user_id, action, old_values) VALUES 
(
    'cfamily',
    163,
    'product_group',
    7,
    1,
    'PATCH',
    '{
    "family": "L0408N3M",
    "type": "4mm mini coreless motor",
    "description": "Precious Metal Commutation",
    "short_description": null,
    "product_group_id": 7,
    "status": 3,
    "user_id": 1,
    "id": 163
    }'
)
,(
    'carticle',
    308,
    'family',
    163,
    1,
    'DELETE',
    '{
    "id": 308,
    "article": "L0408N3M08-750-3.4",
    "description": null,
    "short_description": null,
    "upddate": "2023-03-15T15:59:56",
    "insdate": "2023-02-15T20:17:13",
    "family_id": 163,
    "status": 3,
    "user_id": 1
  }'
);