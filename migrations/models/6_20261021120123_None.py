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
    "updated_by" INT REFERENCES "users" ("id") ON DELETE SET NULL
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
    "state" VARCHAR(15) NOT NULL,
    "city" VARCHAR(15) NOT NULL,
    "zip" VARCHAR(10) NOT NULL,
    "street" VARCHAR(50) NOT NULL,
    "nearby_location" VARCHAR(50),
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "is_closed" BOOL NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_by" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT,
    "updated_by" INT REFERENCES "users" ("id") ON DELETE SET NULL
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
    "created_by" INT NOT NULL REFERENCES "users" ("id") ON DELETE RESTRICT,
    "restaurant_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE RESTRICT,
    "updated_by" INT REFERENCES "users" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "orders" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL,
    "updated_at" TIMESTAMPTZ,
    "order_on" TIMESTAMPTZ NOT NULL,
    "delivered_in" TIMESTAMPTZ,
    "total_price" DECIMAL(10,3) NOT NULL,
    "status" VARCHAR(20) NOT NULL,
    "is_active" BOOL NOT NULL,
    "created_by" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "delivered_by_id" INT REFERENCES "users" ("id") ON DELETE SET NULL,
    "delivery_location_id" INT REFERENCES "address" ("id") ON DELETE SET NULL,
    "restaurant_id" INT NOT NULL REFERENCES "restraunts" ("id") ON DELETE RESTRICT,
    "updated_by" INT REFERENCES "users" ("id") ON DELETE SET NULL,
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
    "updated_at" TIMESTAMPTZ,
    "refresh" UUID NOT NULL UNIQUE,
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
    "g4sef/AVFdoo0="
)
