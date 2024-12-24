import requests
import asyncio

from parser.data import categories_url, game_url, headers


async def get_games_ids(
        url: str,
        headers: dict,
) -> (list, int):
    """
    :param url:
    :param headers:
    :param size: отвечает за кол-во запрашиваемых игр
    :param offset:
    :return: список c id, общее количество игр
    """
    response = requests.get(
        url=url,
        headers=headers
    )
    response = response.json()
    if 'errors' in response.keys():
        x = response['errors']
        raise Exception(f"{x[0]['message']}")
    ans = [idin['id'] for idin in response['data']['categoryGridRetrieve']['concepts']]
    return ans, response['data']['categoryGridRetrieve']['pageInfo']['totalCount']


async def main(
        size: int = 1000,
        offset: int = 1000,
):
    task_list = []
    for i in range(0, 9):
        task_list.append(asyncio.create_task(get_games_ids(
            url=categories_url(
                size=size,
                offset=offset
            ),
            headers=headers,
        )))

    result = await asyncio.gather(*task_list)

    return result

if __name__ == '__main__':

    asyncio.run(main())