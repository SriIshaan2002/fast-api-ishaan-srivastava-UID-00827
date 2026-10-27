from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL,
    "username" VARCHAR(20) NOT NULL,
    "mobile" VARCHAR(13) NOT NULL UNIQUE,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "balance" DECIMAL(10,3) NOT NULL,
    "is_admin" BOOL NOT NULL,
    "updated_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "user" IS 'Represent a user account with profile, balance, and account status.';
CREATE TABLE IF NOT EXISTS "address" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL,
    "city" VARCHAR(50) NOT NULL,
    "street" VARCHAR(100) NOT NULL,
    "house" VARCHAR(50) NOT NULL,
    "zip" VARCHAR(10) NOT NULL,
    "nearby_location" VARCHAR(100),
    "long" DECIMAL(11,8),
    "lat" DECIMAL(10,8),
    "updated_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "address" IS 'Represent a user''s address, including geographic coordinates.';
CREATE TABLE IF NOT EXISTS "restraunt" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL,
    "restaurant_name" VARCHAR(50) NOT NULL UNIQUE,
    "is_closed" BOOL NOT NULL,
    "created_by_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT,
    "location_id_id" INT NOT NULL REFERENCES "address" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "restraunt" IS 'Store restaurant operational records.';
CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL,
    "item_name" VARCHAR(50) NOT NULL,
    "quantity" INT NOT NULL,
    "is_veg" BOOL NOT NULL,
    "description" VARCHAR(500),
    "price" DECIMAL(10,3) NOT NULL,
    "created_by_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT,
    "restaurant_id" INT NOT NULL REFERENCES "restraunt" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "item" IS 'Represent a menu item offered by a restaurant.';
CREATE TABLE IF NOT EXISTS "order" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_active" BOOL NOT NULL,
    "total_price" DECIMAL(10,3) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "created_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL,
    "delivery_location_id" INT REFERENCES "address" ("id") ON DELETE SET NULL,
    "restaurant_id" INT NOT NULL REFERENCES "restraunt" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "order"."status" IS 'PENDING: Pending\nCONFIRMED: Confirmed\nPREPARING: Preparing\nON_THE_WAY: On-the-Way\nDELIVERED: Delivered\nCANCELLED: Cancelled\nRETURNED: Returned';
COMMENT ON TABLE "order" IS 'Represent a customer''s order and its delivery information.';
CREATE TABLE IF NOT EXISTS "order_item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "item_name" VARCHAR(50) NOT NULL,
    "is_veg" BOOL NOT NULL,
    "quantity" INT NOT NULL,
    "discount" INT NOT NULL,
    "price" DECIMAL(10,3) NOT NULL,
    "is_active" BOOL NOT NULL,
    "order_id" INT NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "order_item" IS 'Represent an individual item snapshot associated with an order.';
CREATE TABLE IF NOT EXISTS "owner" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "restraunt_id" INT NOT NULL REFERENCES "restraunt" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_owner_user_id_e30524" UNIQUE ("user_id", "restraunt_id")
);
COMMENT ON TABLE "owner" IS 'Associate a user with restaurants they own.';
CREATE TABLE IF NOT EXISTS "token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "token" VARCHAR(500) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "revoked_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "token" IS 'Store refresh-token records associated with user accounts.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
