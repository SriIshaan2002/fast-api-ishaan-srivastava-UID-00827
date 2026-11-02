from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" ADD "restraunt_city" VARCHAR(20) NOT NULL;
        ALTER TABLE "order" ADD "delivered_in" TIMESTAMPTZ;
        ALTER TABLE "order" ADD "restraunt_name" VARCHAR(20) NOT NULL;
        ALTER TABLE "order" ADD "order_on" TIMESTAMPTZ NOT NULL DEFAULT NULL;
        ALTER TABLE "order" ADD "restraunt_street" VARCHAR(20) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order" DROP COLUMN "restraunt_city";
        ALTER TABLE "order" DROP COLUMN "delivered_in";
        ALTER TABLE "order" DROP COLUMN "restraunt_name";
        ALTER TABLE "order" DROP COLUMN "order_on";
        ALTER TABLE "order" DROP COLUMN "restraunt_street";"""


MODELS_STATE = (
    "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"
    "zcCJ6CdoBdc8mveUMsDv/wN2VD08"
)
