from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "restraunts" DROP CONSTRAINT IF EXISTS "fk_restraun_users_223073d0";
        ALTER TABLE "orders" DROP CONSTRAINT IF EXISTS "fk_orders_users_d2492591";
        ALTER TABLE "items" DROP CONSTRAINT IF EXISTS "fk_items_users_ed7e9865";
        ALTER TABLE "addresses" ADD "updated_at" TIMESTAMPTZ;
        ALTER TABLE "items" DROP COLUMN "updated_by_id";
        ALTER TABLE "orders" DROP COLUMN "updated_by_id";
        ALTER TABLE "restraunts" DROP COLUMN "updated_by_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" ADD "updated_by_id" INT;
        ALTER TABLE "orders" ADD "updated_by_id" INT;
        ALTER TABLE "addresses" DROP COLUMN "updated_at";
        ALTER TABLE "restraunts" ADD "updated_by_id" INT;
        ALTER TABLE "items" ADD CONSTRAINT "fk_items_users_ed7e9865" FOREIGN KEY ("updated_by_id") REFERENCES "users" ("id") ON DELETE SET NULL;
        ALTER TABLE "orders" ADD CONSTRAINT "fk_orders_users_d2492591" FOREIGN KEY ("updated_by_id") REFERENCES "users" ("id") ON DELETE SET NULL;
        ALTER TABLE "restraunts" ADD CONSTRAINT "fk_restraun_users_223073d0" FOREIGN KEY ("updated_by_id") REFERENCES "users" ("id") ON DELETE SET NULL;"""


MODELS_STATE = (
    "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"
    "vJbXrlkTVwKxKlTpmj9O1fgD290g=="
)
