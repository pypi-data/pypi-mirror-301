import asyncio
from src import __version__


async def main():
    print(__version__)


if __name__ == '__main__':
    asyncio.run(main())
