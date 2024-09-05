import asyncio
import logging
import sys

from t0d0d0d0.bot.bot import main

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
