from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ALTER COLUMN "revoked_at" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ALTER COLUMN "revoked_at" SET NOT NULL;"""


MODELS_STATE = (
    "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"
    "g="
)
