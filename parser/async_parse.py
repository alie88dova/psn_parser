import json
import re
import time

import requests
import asyncio

from parser.data import categories_url, game_url, headers as head
from itertools import chain
from aiohttp import ClientSession


storage = {}


async def get_response(
        url,
        headers,
        proxy=None
):
    async with storage['session'].get(
        url=url,
        headers=headers,
        proxy=proxy
    ) as response:
        return await response.json()




async def get_games_ids(
        url: str,
        headers: dict,
        proxy=None
) -> list:
    """
    :param proxy:
    :param url:
    :param headers:
    :param size: отвечает за кол-во запрашиваемых игр
    :param offset:
    :return: список c id, общее количество игр
    """
    print(time.strftime('%X'))
    response = await get_response(
        url=url,
        headers=headers,
        proxy=proxy
    )
    print(time.strftime('%X'), 'end')
    if 'errors' in response.keys():
        x = response['errors']
        raise Exception(f"{x[0]['message']}")
    ans = [idin['id'] for idin in response['data']['categoryGridRetrieve']['concepts']]
    return ans


def check_connection(
        headers,
        proxy=None
) -> int:
    """Проверяет доступен ли для запросов сайт PSN, и возвращает кол-вл игр в каталоге"""
    response = requests.get(
        url=categories_url(1, 0),
        headers=headers,
        proxies=proxy
    )
    response = response.json()
    if 'errors' in response.keys():
        x = response['errors']
        raise Exception(f"{x[0]['message']}")
    return int(response['data']['categoryGridRetrieve']['pageInfo']['totalCount'])


async def get_info(
        url: str,
        headers: dict,
        proxy=None
) -> list[dict]:
    print('Start load info')
    response = await get_response(
        url=url,
        headers=headers,
        proxy=proxy
    )
    print('End Load Info')
    response = response['data']['conceptRetrieve']['products']
    ans = []
    for game in response:
        if game['webctas'] != []:
            x = game['webctas'][0]['price']
            name = game['name']
            avaible_marker = "AVAILABLE" if game['webctas'][0]['type'] != "UNAVAILABLE" else "UNAVAILABLE"
            ans.append({
                "basePriceValue": x['basePriceValue'],
                "discountedValue": x["discountedValue"],
                "endTime": x['endTime'],
                "name": name,
                "type": avaible_marker,
                "discont_percent": 0 if x['discountText'] is None or x['discountText'] == "Dahil" else int(
                    re.findall(r'\d+', x['discountText'])[0])
            })
    return ans


async def get_all_games(
        size: int = 1000,
        offset: int = 1000,
        proxy=None,
):
    total = check_connection(head, proxy=proxy)
    print(total)
    task_list = []
    for i in range(0, 10):
        print(offset*i)
        if size + offset*i > total:
            size = total - offset*i
        task_list.append(asyncio.create_task(get_games_ids(
            url=categories_url(
                size=size,
                offset=offset*i
            ),
            headers=head,
            proxy=proxy
        )))
    result = await asyncio.gather(*task_list)
    return list(chain.from_iterable(result))


async def get_all_game_info(games_id: list, proxy):
    task_list = []
    for game_id in games_id:
        task_list.append(asyncio.create_task(
            get_info(
                url=game_url(game_id),
                headers=head,
                proxy=proxy
            )
        ))
    result = await asyncio.gather(*task_list)

    return list(chain.from_iterable(result))


async def main():
    storage['session'] = ClientSession()
    async with storage['session']:
        game_list = await get_all_games(

        )
        ans = await get_all_game_info(
            game_list,
            proxy=None
        )
        return ans


if __name__ == '__main__':
    full_games_json = asyncio.run(main())
    print(len(full_games_json))
    with open('all_games.json', 'w') as f:
        f.writelines(json.dumps(full_games_json))

