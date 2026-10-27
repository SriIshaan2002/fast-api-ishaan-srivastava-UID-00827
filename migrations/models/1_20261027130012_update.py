from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "owner" ADD "created_at" TIMESTAMPTZ NOT NULL DEFAULT NULL;
        ALTER TABLE "owner" ADD "is_active" BOOL NOT NULL DEFAULT True;
        ALTER TABLE "owner" ADD "updated_at" TIMESTAMPTZ;
        ALTER TABLE "owner" ADD "updated_by_id" INT;
        ALTER TABLE "owner" ADD CONSTRAINT "fk_owner_user_cd37b1ad" FOREIGN KEY ("updated_by_id") REFERENCES "user" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "owner" DROP CONSTRAINT IF EXISTS "fk_owner_user_cd37b1ad";
        ALTER TABLE "owner" DROP COLUMN "created_at";
        ALTER TABLE "owner" DROP COLUMN "is_active";
        ALTER TABLE "owner" DROP COLUMN "updated_at";
        ALTER TABLE "owner" DROP COLUMN "updated_by_id";"""


MODELS_STATE = (
    "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"
    "1fRBu/uA=="
)
