import re
import time

import requests
import asyncio

from parser.data import categories_url, game_url, headers as head
from itertools import chain


async def get_response(
        url,
        headers,
        proxy=None
):
    response = requests.get(
        url=url,
        headers=headers,
        proxies=proxy
    )
    return response


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
    response = response.json()
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
        url:str,
        headers: dict,
        proxy = None
) -> list[dict]:

    response = requests.get(
        url=url,
        headers=headers,
        proxies=proxy
    )
    response = response.json()['data']['conceptRetrieve']['products']
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


if __name__ == '__main__':
    a = asyncio.run(get_all_games(

    ))
    print(len(a))
    all_games_json = []
    for game_id in a:
        print(game_id)
        all_games_json.append(
            asyncio.run(get_info(
                game_url(game_id),
                head,
                proxy=None
                )
            )
        )
    all_games_json = list(chain.from_iterable(all_games_json))
    print(len(all_games_json))


