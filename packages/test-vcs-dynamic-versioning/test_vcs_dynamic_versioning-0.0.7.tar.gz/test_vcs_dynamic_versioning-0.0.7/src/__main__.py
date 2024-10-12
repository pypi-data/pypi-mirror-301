import asyncio
from importlib.metadata import version

package_version = version(__package__)


async def main():
    print(package_version)


if __name__ == '__main__':
    asyncio.run(main())
