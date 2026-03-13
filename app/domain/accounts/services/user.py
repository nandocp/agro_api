async def login(
    self, email: str, password: str, account_id: UUID
) -> tuple[User, str]:
    user = await self.repo.get_by_email_and_account(email, account_id)

    if not user:
        raise InvalidCredentialsError

    if user.locked_at:
        raise AccountLockedError

    if not user.confirmed_at:
        raise EmailNotConfirmedError

    if not verify_password(password, user.password):
        user.failed_attempts += 1
        if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_at = datetime.utcnow()
        await self.repo.save(user)
        raise InvalidCredentialsError

    # login bem sucedido
    user.last_sign_in_at = user.current_sign_in_at
    user.current_sign_in_at = datetime.utcnow()
    user.sign_in_count += 1
    user.failed_attempts = 0
    user.jti = uuid4()

    await self.repo.save(user)
    token = create_access_token(subject=user.id, jti=user.jti)
    return user, token


async def logout(self, user: User) -> None:
    user.jti = None  # invalida o token atual
    await self.repo.save(user)
