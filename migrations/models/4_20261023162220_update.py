from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" DROP COLUMN "revoked_at";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ADD "revoked_at" TIMESTAMPTZ;"""


MODELS_STATE = (
    "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"
    "UEc4"
)
