from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL,
    "mobile" VARCHAR(13) NOT NULL UNIQUE,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "balance" DECIMAL(10,3) NOT NULL,
    "is_admin" BOOL NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "users" IS 'Represent a user account with profile, balance, and account status.';
CREATE TABLE IF NOT EXISTS "addresses" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "city" VARCHAR(50) NOT NULL,
    "street" VARCHAR(50) NOT NULL,
    "house" VARCHAR(20) NOT NULL,
    "zip" VARCHAR(10) NOT NULL,
    "nearby_location" VARCHAR(50),
    "long" DECIMAL(11,8),
    "lat" DECIMAL(10,8),
    "is_active" BOOL NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT
);
COMMENT ON TABLE "addresses" IS 'Represent a user''s address, including geographic coordinates.';
CREATE TABLE IF NOT EXISTS "restraunts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "restaurant_name" VARCHAR(20) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_closed" BOOL NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_by_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT,
    "location_id_id" INT NOT NULL REFERENCES "addresses" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "restraunts" IS 'Store refresh-token records associated with user accounts.';
CREATE TABLE IF NOT EXISTS "items" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "item_name" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "quantity" INT NOT NULL,
    "is_veg" BOOL NOT NULL,
    "description" VARCHAR(255),
    "price" DECIMAL(10,3) NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_by_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT,
    "restaurant_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "items" IS 'Represent a menu item offered by a restaurant.';
CREATE TABLE IF NOT EXISTS "orders" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "delivered_in" TIMESTAMPTZ,
    "total_price" DECIMAL(10,3) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "delivered_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "delivery_location_id" INT REFERENCES "addresses" ("id") ON DELETE SET NULL,
    "restaurant_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "orders"."status" IS 'PENDING: Pending\nCONFIRMED: Confirmed\nPREPARING: Preparing\nON_THE_WAY: On-the-Way\nDELIVERED: Delivered\nCANCELLED: Cancelled\nRETURNED: Returned';
COMMENT ON TABLE "orders" IS 'Represent a customer''s order and its delivery information.';
CREATE TABLE IF NOT EXISTS "order_items" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "item_name" VARCHAR(20) NOT NULL,
    "is_veg" BOOL NOT NULL,
    "quantity" INT NOT NULL,
    "discount" INT NOT NULL,
    "price" DECIMAL(10,3) NOT NULL,
    "is_active" BOOL NOT NULL,
    "order_id" INT NOT NULL REFERENCES "orders" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "order_items" IS 'Represent an individual item snapshot associated with an order.';
CREATE TABLE IF NOT EXISTS "owners" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "restraunt_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_owners_user_id_36971a" UNIQUE ("user_id", "restraunt_id")
);
COMMENT ON TABLE "owners" IS 'Associate users with restaurants they own.';
CREATE TABLE IF NOT EXISTS "tokens" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uuid" UUID NOT NULL UNIQUE,
    "token" VARCHAR(500) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "revoked_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "tokens" IS 'Store refresh-token records associated with user accounts.';
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
    "3c1ukvw87eCGRwmfUiT48n+OB/yt"
)
