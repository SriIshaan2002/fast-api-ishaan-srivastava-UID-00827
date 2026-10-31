from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "address" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "address" ALTER COLUMN "updated_at" SET NOT NULL;
        ALTER TABLE "item" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "item" ALTER COLUMN "updated_at" SET NOT NULL;
        ALTER TABLE "order" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "order" ALTER COLUMN "updated_at" SET NOT NULL;
        ALTER TABLE "owner" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "owner" ALTER COLUMN "updated_at" SET NOT NULL;
        ALTER TABLE "restraunt" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "restraunt" ALTER COLUMN "updated_at" SET NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "updated_at" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "item" ALTER COLUMN "updated_at" DROP NOT NULL;
        ALTER TABLE "item" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "updated_at" DROP NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "order" ALTER COLUMN "updated_at" DROP NOT NULL;
        ALTER TABLE "order" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "owner" ALTER COLUMN "updated_at" DROP NOT NULL;
        ALTER TABLE "owner" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "address" ALTER COLUMN "updated_at" DROP NOT NULL;
        ALTER TABLE "address" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;
        ALTER TABLE "restraunt" ALTER COLUMN "updated_at" DROP NOT NULL;
        ALTER TABLE "restraunt" ALTER COLUMN "updated_at" TYPE TIMESTAMPTZ USING "updated_at"::TIMESTAMPTZ;"""


MODELS_STATE = (
    "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"
    "9up9cMnJjMhHZwzaPDT6mW/P4v5YzhYA=="
)
