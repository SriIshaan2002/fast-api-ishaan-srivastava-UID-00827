from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ADD "revoked_at" TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" DROP COLUMN "revoked_at";"""


MODELS_STATE = (
    "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"
    "ycjzDm5FJPApgwJf/w9gGeIN"
)
