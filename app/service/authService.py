"""
This module contains the business logic for user authentication.

It handles user signup, login, refresh-token validation, and logout.
"""
from tortoise.exceptions import IntegrityError
from constants import AUTH_ERRORS, GENERAL
from app.auth import jwt_handler
from app.models import *
from app.schemas.token import TokenResponse

class AuthServiceError(Exception):
    """Represent an authentication-related service error."""
    def __init__(self, status_code: int, detail: str):
        """Initialize the error with an HTTP status code and detail."""
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class AuthService:
    """Provide business logic for authentication operations."""
    @staticmethod
    async def signup(user_data) -> TokenResponse:
        """
        Register a new user and generate authentication tokens.

        Args:
            user_data: Validated user registration data.

        Returns:
            Access token and refresh-token UUID.

        Raises:
            AuthServiceError: If the email is already registered.
        """
        user_data.email = user_data.email.lower()
        user_exists = await User.filter(email=user_data.email).exists()
        if user_exists:
            raise AuthServiceError(400, AUTH_ERRORS.registered_email)
        try:
            created_user = await User.create(**user_data.model_dump())
        except IntegrityError as exc:
            raise AuthServiceError(
                400, AUTH_ERRORS.registered_email
            ) from exc
        return await AuthService._generate_tokens(
            user=created_user,
            is_admin=created_user.is_admin,
            is_owner=False,
        )

    @staticmethod
    async def login(user_data) -> TokenResponse:
        """
        Authenticate a user and generate authentication tokens.

        Args:
            user_data: Validated login credentials.

        Returns:
            Access token and refresh-token UUID.

        Raises:
            AuthServiceError: If the user does not exist or the
                supplied password is invalid.
        """
        email = user_data.email.lower()
        existing_user = await User.filter(email=email).first()
        if not existing_user:
            raise AuthServiceError(404, AUTH_ERRORS.user_not_found)
        if existing_user.password != user_data.password:
            raise AuthServiceError(401, AUTH_ERRORS.invalid_password)
        if not existing_user.is_active:
            raise AuthServiceError(403, AUTH_ERRORS.user_not_found)
        is_owner = await Owner.filter(
            user_id=existing_user.id
        ).exists()
        return await AuthService._generate_tokens(
            user=existing_user,
            is_admin=existing_user.is_admin,
            is_owner=is_owner,
        )
    @staticmethod
    async def refresh(auth_uuid: str) -> dict:
        """
        Validate a refresh token and generate a new access token.

        Args:
            auth_uuid: UUID identifying the stored refresh token.

        Returns:
            A dictionary containing the new access token.

        Raises:
            AuthServiceError: If the refresh token is invalid or
                its associated user is unavailable.
        """
        existing_token = await Token.filter(uuid=auth_uuid).first()
        if (
            not existing_token
            or existing_token.revoked_at is not None
        ):
            raise AuthServiceError(401, AUTH_ERRORS.invalid_token)
        payload = jwt_handler.decode_and_verify_token(
            existing_token.token
        )
        if not payload:
            raise AuthServiceError(401, AUTH_ERRORS.invalid_token)
        user = await User.filter(
            id=existing_token.user_id
        ).first()
        if not user or not user.is_active:
            raise AuthServiceError(401, AUTH_ERRORS.user_inactive)
        is_owner = await Owner.filter(user_id=user.id).exists()
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            username=user.username,
            is_admin=user.is_admin,
            is_owner=is_owner,
        )
        return {GENERAL.access_token: access_token}
    @staticmethod
    async def logout(auth_uuid: str) -> dict:
        """
        Invalidate a stored refresh-token session.
        Args:
            auth_uuid: UUID identifying the stored refresh token.

        Returns:
            A message confirming logout.

        Raises:
            AuthServiceError: If the session does not exist.
        """
        deleted_count = await Token.filter(
            uuid=auth_uuid
        ).delete()
        if deleted_count == 0:
            raise AuthServiceError(
                404,
                "Session already logged out or invalid UUID.",
            )
        return {"detail": AUTH_ERRORS.user_inactive}
    
    @staticmethod
    async def _generate_tokens(user: User, is_admin: bool, is_owner: bool) -> TokenResponse:
        """
        Generate and persist authentication tokens for a user.

        Args:
            user: User for whom the tokens are generated.
            is_admin: Whether the user has administrator privileges.
            is_owner: Whether the user is a restaurant owner.

        Returns:
            Access token and refresh-token UUID.
        """
        access_token = jwt_handler.create_access_token(
            user_id=user.id,
            username=user.username,
            is_admin=is_admin,
            is_owner=is_owner,
        )
        refresh_token, token_uuid = (
            jwt_handler.create_refresh_token(
                user_id=user.id,
                username=user.username,
                is_admin=is_admin,
                is_owner=is_owner,
            )
        )
        await Token.create(
            user_id=user.id,
            uuid=token_uuid,
            token=refresh_token,
        )
        return TokenResponse(
            access_token=access_token,
            user_uuid=str(token_uuid),
        )
    