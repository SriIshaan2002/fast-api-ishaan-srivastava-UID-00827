from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ADD "token" VARCHAR(255) NOT NULL;
        ALTER TABLE "token" RENAME COLUMN "refresh" TO "uuid";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" RENAME COLUMN "uuid" TO "refresh";
        ALTER TABLE "token" DROP COLUMN "token";"""


MODELS_STATE = (
    "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"
    "c="
)
