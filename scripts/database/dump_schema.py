import subprocess

from config.settings import settings


def dump_schema(output: str = 'migrations/schema.sql') -> None:
    url = settings.DATABASE_URL.replace(
        'postgresql+psycopg://', 'postgresql://'
    )
    result = subprocess.run(
        [
            'pg_dump',
            '--schema-only',
            '--no-owner',
            '--no-privileges',
            '--no-comments',
            url,
            '-f',
            output,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        print(f'✓ Schema dumped to {output}')
    else:
        raise RuntimeError(f'Schema dump failed: {result.stderr}')


if __name__ == '__main__':
    dump_schema()
