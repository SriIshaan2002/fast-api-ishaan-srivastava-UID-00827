from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "mobile" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "mobile" SET NOT NULL;"""


MODELS_STATE = (
    "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"
    "k="
)
