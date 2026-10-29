"""
This module contains the business logic for user authentication.

It handles user signup, login, refresh-token validation, and logout.
"""

from tortoise.exceptions import IntegrityError

from app.auth import jwt_handler
from app.exception.AuthException import (
    AccountInactiveError,
    InvalidPasswordError,
    InvalidTokenError,
    RegisteredEmail,
    SessionNotFoundError,
    UserNotFoundError,
)
from app.models import Token, User
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin
from app.util import hash_password, verify_password
from constants import AUTH_ERRORS, AUTH_SUCCESS, GENERAL


class AuthService:
    """Provide business logic for authentication operations."""

    @staticmethod
    async def signup(user_data: UserCreate) -> TokenResponse:
        """
        Register a new user account.

        Args:
                user_data: Validated signup credentials.

        Returns:
                Access token and refresh-token UUID.

        Raises:
                RegistrationError: If the email already exists.
        """
        email_clean = user_data.email.lower()

        existing_user = await User.filter(email=email_clean).first()
        if existing_user:
            raise RegisteredEmail(error=AUTH_ERRORS.registered_email)

        user_dump = user_data.model_dump()
        user_dump["email"] = email_clean
        user_dump["password"] = hash_password(password=user_data.password)
        try:
            created_user = await User.create(**user_dump)
        except IntegrityError as exc:
            raise RegisteredEmail() from exc
        return await AuthService._generate_tokens(
            user=created_user, is_admin=created_user.is_admin
        )

    @staticmethod
    async def login(user_data: UserLogin) -> TokenResponse:
        """
        Authenticate a user and generate authentication tokens.

        Args:
            user_data: Validated login credentials.

        Returns:
            Access token and refresh-token UUID.

        Raises:
            UserNotFoundError: If the user does not exist.
            InvalidPasswordError: If the password matches fail.
            AccountInactiveError: If the account is deactivated.
        """
        email = user_data.email
        existing_user = await User.filter(email=email).first()
        if not existing_user:
            raise UserNotFoundError()
        if not verify_password(user_data.password, existing_user.password):
            raise InvalidPasswordError()
        if not existing_user.is_active:
            raise AccountInactiveError()
        return await AuthService._generate_tokens(
            user=existing_user,
            is_admin=existing_user.is_admin,
        )

    @staticmethod
    async def refresh(auth_uuid: str, user_id: int) -> dict:
        """
        Validate a refresh token and generate a new access token.
        Args:
            auth_uuid: UUID as the jti for refresh token in the db

        Returns:
            Access token and refresh-token UUID.

        Raises:
            InvalidTokenError

        """
        existing_token = await Token.filter(uuid=auth_uuid, user_id=user_id).first()
        if not existing_token or existing_token.revoked_at is not None:
            raise InvalidTokenError()
        user = await User.filter(id=user_id).first()
        if not user or not user.is_active:
            raise InvalidTokenError(detail=AUTH_ERRORS.user_inactive)
        access_token = jwt_handler.create_access_token(
            user_id=user_id,
            is_admin=user.is_admin,
        )
        return {GENERAL.access_token: access_token}

    @staticmethod
    async def logout(auth_uuid: str) -> dict:
        """
        Invalidate a stored refresh-token session.
        Args:
            auth_uuid: UUID as the jti for refresh token in the db

        Returns:
            Dictionary for logged out message

        Raises:
            SessionNotFoundError
        """
        deleted_count = await Token.filter(uuid=auth_uuid).delete()
        if deleted_count == 0:
            raise SessionNotFoundError()
        return {"detail": AUTH_SUCCESS.logged_out}

    @staticmethod
    async def reactivate(user_data: UserLogin) -> TokenResponse:
        """
        Reactivate a soft-deleted account and return authentication tokens.
        Args:
                auth_uuid: UUID as the jti for refresh token in the db

        Returns:
            TokenResponse

        Raises:
            UserNotFoundError
            InvalidPasswordError
        """
        email = user_data.email.lower()
        existing_user = await User.filter(email=email).first()
        if not existing_user:
            raise UserNotFoundError()
        if not verify_password(user_data.password, existing_user.password):
            raise InvalidPasswordError()
        if not existing_user.is_active:
            existing_user.is_active = True
            await existing_user.save(update_fields=["is_active"])
        return await AuthService._generate_tokens(
            user=existing_user, is_admin=existing_user.is_admin
        )

    @staticmethod
    async def _generate_tokens(user: User, is_admin: bool) -> TokenResponse:
        """
        Generate and persist authentication tokens for a user.
        Returns:
            TokenResponse

        """
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            is_admin=is_admin,
        )
        token_uuid, expire = jwt_handler.create_refresh_token()
        await Token.create(user_id=user.id, uuid=token_uuid, exp_at=expire)
        return TokenResponse(
            access_token=access_token,
            user_uuid=str(token_uuid),
        )
