from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "item" ALTER COLUMN "price" TYPE INT USING "price"::INT;
        ALTER TABLE "order_item" ADD "item_id" INT NOT NULL;
        ALTER TABLE "order_item" ALTER COLUMN "price" TYPE INT USING "price"::INT;
        ALTER TABLE "order_item" ADD CONSTRAINT "fk_order_it_item_f9ed96ce" FOREIGN KEY ("item_id") REFERENCES "item" ("id") ON DELETE RESTRICT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "order_item" DROP CONSTRAINT IF EXISTS "fk_order_it_item_f9ed96ce";
        ALTER TABLE "item" ALTER COLUMN "price" TYPE DECIMAL(10,3) USING "price"::DECIMAL(10,3);
        ALTER TABLE "item" ALTER COLUMN "price" TYPE DECIMAL(10,3) USING "price"::DECIMAL(10,3);
        ALTER TABLE "order_item" DROP COLUMN "item_id";
        ALTER TABLE "order_item" ALTER COLUMN "price" TYPE DECIMAL(10,3) USING "price"::DECIMAL(10,3);
        ALTER TABLE "order_item" ALTER COLUMN "price" TYPE DECIMAL(10,3) USING "price"::DECIMAL(10,3);"""


MODELS_STATE = (
    "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"
    "9BP0BDc8mveUMsAf/weJQtM+"
)
