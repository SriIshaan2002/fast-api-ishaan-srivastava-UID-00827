from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ALTER COLUMN "token" TYPE VARCHAR(500) USING "token"::VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ALTER COLUMN "token" TYPE VARCHAR(255) USING "token"::VARCHAR(255);"""


MODELS_STATE = (
    "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"
    "wReJ+pYs//A6+gMeI="
)
