import time

import requests
import asyncio

from parser.data import categories_url, game_url, headers


async def get_games_ids(
        url: str,
        headers: dict,
        proxy=None
) -> (list, int):
    """
    :param proxy:
    :param url:
    :param headers:
    :param size: отвечает за кол-во запрашиваемых игр
    :param offset:
    :return: список c id, общее количество игр
    """
    print(time.strftime('%X'))
    response = requests.get(
        url=url,
        headers=headers,
        proxies=proxy
    )
    print(time.strftime('%X'), 'end')
    response = response.json()
    if 'errors' in response.keys():
        x = response['errors']
        raise Exception(f"{x[0]['message']}")
    ans = [idin['id'] for idin in response['data']['categoryGridRetrieve']['concepts']]
    return ans, response['data']['categoryGridRetrieve']['pageInfo']['totalCount']


def check_connection(proxy=None) -> int:
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


async def main(
        size: int = 1000,
        offset: int = 1000,
        proxy=None,
):
    total = check_connection(proxy)
    task_list = []
    for i in range(0, 9):
        if size + offset*i > total:
            size = total - offset*i
        task_list.append(asyncio.create_task(get_games_ids(
            url=categories_url(
                size=size,
                offset=offset*i
            ),
            headers=headers,
            proxy=proxy
        )))
    result = await asyncio.gather(*task_list)

    return result

if __name__ == '__main__':
    asyncio.run(main())