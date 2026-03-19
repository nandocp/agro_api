async def run(session: AsyncSession) -> None:
    print('Seeding permissions...')
    permission_map = await seed_permissions(session)

    print('Seeding roles...')
    await seed_roles(session, permission_map)

    print('Seeding superuser...')
    await seed_superuser(session)

    print('Seeding organism traits...')
    await seed_organism_traits(session)

    await session.commit()
    print('✓ Seed completed successfully.')


if __name__ == '__main__':

    async def main():
        engine = create_async_engine(settings.DATABASE_URL)
        async with AsyncSession(engine, expire_on_commit=False) as session:
            await run(session)

    asyncio.run(main())
