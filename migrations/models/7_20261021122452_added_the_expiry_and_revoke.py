from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "items" ALTER COLUMN "created_by" TYPE INT USING "created_by"::INT;
        ALTER TABLE "orders" DROP COLUMN "order_on";
        ALTER TABLE "orders" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "orders" ALTER COLUMN "created_by" TYPE INT USING "created_by"::INT;
        ALTER TABLE "restraunts" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "restraunts" ALTER COLUMN "created_by" TYPE INT USING "created_by"::INT;
        ALTER TABLE "token" ADD COLUMN "created_at" TIMESTAMPTZ;
        ALTER TABLE "token" RENAME COLUMN "updated_at" TO "revoked_at";
        ALTER TABLE "users" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "items" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "items" ALTER COLUMN "created_by" TYPE INT USING "created_by"::INT;
        ALTER TABLE "users" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "orders" ADD "order_on" TIMESTAMPTZ NOT NULL DEFAULT NULL;
        ALTER TABLE "orders" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "orders" ALTER COLUMN "created_by" TYPE INT USING "created_by"::INT;
        ALTER TABLE "token" RENAME COLUMN "revoked_at" TO "updated_at";
        ALTER TABLE "token" DROP COLUMN "created_at";
        ALTER TABLE "restraunts" ALTER COLUMN "updated_by" TYPE INT USING "updated_by"::INT;
        ALTER TABLE "restraunts" ALTER COLUMN "created_by" TYPE INT USING "created_by"::INT;"""


MODELS_STATE = (
    "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"
    "PFXv4H2V2sOw=="
)
