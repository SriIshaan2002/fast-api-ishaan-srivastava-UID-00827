from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "email" TYPE VARCHAR(50) USING "email"::VARCHAR(50);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "email" TYPE VARCHAR(254) USING "email"::VARCHAR(254);"""


MODELS_STATE = (
    "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"
    "sw6uRZTwIRWCz/8CLPT8Cw=="
)
