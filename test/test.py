import asyncio
import time

from parser.sync_parse import get_info, get_games_ids
from parser.async_parse import main

if __name__ == '__main__':
    print(time.strftime('%X'))
    asyncio.run(main(

    ))
    print(time.strftime('%X'))
