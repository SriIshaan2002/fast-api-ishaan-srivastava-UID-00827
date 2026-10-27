from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
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
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
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
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "restaurant_name" VARCHAR(50) NOT NULL UNIQUE,
    "is_closed" BOOL NOT NULL,
    "created_by_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE RESTRICT,
    "location_id_id" INT NOT NULL REFERENCES "address" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);
COMMENT ON TABLE "restraunt" IS 'Store restaurant operational records.';
CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
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
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
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
COMMENT ON TABLE "owner" IS 'Associate User with restaurants they own.';
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
    "/7ck3IO76W0yrU87uOXRvadU/339H3YFyoM="
)
