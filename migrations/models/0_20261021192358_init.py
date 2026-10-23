from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20) NOT NULL,
    "mobile" VARCHAR(13) NOT NULL UNIQUE,
    "email" VARCHAR(254) NOT NULL UNIQUE,
    "balance" DECIMAL(10,3) NOT NULL,
    "is_admin" BOOL NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "address" (
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
CREATE TABLE IF NOT EXISTS "restraunts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "restaurant_name" VARCHAR(20) NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_closed" BOOL NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_by_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT,
    "location_id_id" INT NOT NULL REFERENCES "address" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL
);
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
    "delivery_location_id" INT REFERENCES "address" ("id") ON DELETE SET NULL,
    "restaurant_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE RESTRICT,
    "updated_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "orders"."status" IS 'PENDING: Pending\nCONFIRMED: Confirmed\nPREPARING: Preparing\nON_THE_WAY: On-the-Way\nDELIVERED: Delivered\nCANCELLED: Cancelled\nRETURNED: Returned';
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
CREATE TABLE IF NOT EXISTS "owners" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "restraunt_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_owners_user_id_36971a" UNIQUE ("user_id", "restraunt_id")
);
CREATE TABLE IF NOT EXISTS "token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "refresh" UUID NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL,
    "revoked_at" TIMESTAMPTZ,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
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
