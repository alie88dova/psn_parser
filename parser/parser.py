import requests


def get_games_ids(
        size: int = 1000,
        offset: int = 0
) -> (list, int):
    """
    :param size: отвечает за кол-во запрашиваемых игр
    :param offset:
    :return: список c id, общее количество игр
    """
    if size > 1000 or size <= 0:
        raise Exception("Size must be none 0 and lower 1000")

    url = f"https://web.np.playstation.com/api/graphql/v1//op?operationName=categoryGridRetrieve&variables=%7B%22id%22%3A%2228c9c2b2-cecc-415c-9a08-482a605cb104%22%2C%22pageArgs%22%3A%7B%22size%22%3A{size}%2C%22offset%22%3A{offset}%7D%2C%22sortBy%22%3Anull%2C%22filterBy%22%3A%5B%5D%2C%22facetOptions%22%3A%5B%22ageRating%22%2C%22conceptCompatibilityNotices%22%2C%22conceptGenres%22%2C%22conceptReleaseDate%22%2C%22conceptVrCompatibility%22%2C%22webBasePrice%22%2C%22productCompatibilityNotices%22%2C%22productGenres%22%2C%22productReleaseDate%22%2C%22productVrCompatibility%22%2C%22storeDisplayClassification%22%2C%22targetPlatforms%22%5D%2C%22maxResults%22%3Anull%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%224ce7d410a4db2c8b635a48c1dcec375906ff63b19dadd87e073f8fd0c0481d35%22%7D%7D"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ru,en-US;q=0.9,en;q=0.8",
        "apollographql-client-name": "@sie-ppr-web-store/app",
        "apollographql-client-version": "@sie-ppr-web-store/app@0.91.0",
        "content-type": "application/json",
        "cookie": "sbsd_ss=ab8e18ef4e; AKA_A2=A; _gcl_au=1.1.1515880548.1734926676; s_fid=101061788948545B-114A7B53922D8D7E; s_cc=true; _ga=GA1.1.684424273.1734926714; s_sq=%5B%5BB%5D%5D; _ga_7NX8QXLJQK=GS1.1.1734926713.1.1.1734926727.0.0.0; _ga_Y01S4T0NK9=GS1.1.1734926713.1.1.1734926727.0.0.0; pdcRedirect=store; sbsd_o=F90CB938EE8EB36066C557543044B67CF8EFBC3AFA3FAC0F76A6A3F0020F1777~s57RSnenqgjL5pCzEcboTFtdeUNlVVv8aKgd6j2NTK20y+tG2/+Lrm5LMqVWdI3qzDis1Lk1tG9I7CR3+uq3jf7lY3OiE5loHcbsTXFq6Nhjf4tsDNacTkcqmEtsMPawEZI87bUQ/JrHYfubhnMgb89p8FtxvddTOTG8p0K3xCEW5l5cy/7rjuK07xHjThc+Fuql8ODrUnLDrpSPDMoE4oJCNu9lmNuNqcC3bVdkwjHs=; sbsd=sINA4LYy9tXp1Cg+Y8d8J0ny2MLJ1EsYYdpj1ZNxGB/2CxH8n2CCXWAOW76z1oNAB2gI7YFbYqU93Wy7KcTQ2M4TkFEIs6Au14x0qhzej5gE0enc1AIUxpcQ/UtiVsl+/S8ONBRhdDXFWhzU0dhQ4W5W23DJOFs+fYYevNSwFX+HpJnw1XpNXrEACcTK3XGZHfRAdWZFprHORFEvhwYbtp8N0oy4Ke1RxEGAkoOQPlbVX74QM7rkkNUkRUwDtNLt/hVyRUe8c/5DlMrIP0Z6BgE+1GNzB0VJts9KKR/Kyexk=; bm_sz=2AA859BE282DE6ABAF6ECC0944A628B4~YAAQmANJF+a5OKqTAQAAW/Hl8RpJW8CVaBG6t8xg01W1QM0jTfApM8IsKx8fN7tlyT9jlmQ7Fn3uiYDRU+himQox8GqYwBqohAS3VuA3jL025Lv2e4qtxgGFPCtLwZMUnPOoCAoaBInqlbee6JDw8lmy9RQMqS5aoIIudYSDW3o/pPVO/oVj9J3DK5AUGdjaAXK5RpNgtA1Tp7VkHhTGPFdJaFxDlKDxamKphHhMACrs/ifaX7TF6yppU5dasHH43VSZXntjQgDFr80gDnvAw1sTUKztauZyhRfuu0vgt9bulCGJr5YEufZ9zZ5usJlQDsVp8LJ07qr7s3yx2sHrtWssH781ZX5rJo2kglEm9RVYq0JgWSaxQYYHWypdhNrx4JiaTXBHDE04b12O3Ng6Kci9b1+296Uqbzn7dLGjs+/KmzybzhUaPn+QBfAWEis5rj+K1lbKAxeSLyxxobb+MD3EXcjLXFppbAphcdu8H+DARlayg4PMDd0ZGu6uw6DfZMQsPMTh4CjsUlBJv1WJT9mbIo5kV0jXeiIOwG4heB/XUPoYvgFor/Gpl/yxAQ==~4539201~3621955; bm_lso=F90CB938EE8EB36066C557543044B67CF8EFBC3AFA3FAC0F76A6A3F0020F1777~s57RSnenqgjL5pCzEcboTFtdeUNlVVv8aKgd6j2NTK20y+tG2/+Lrm5LMqVWdI3qzDis1Lk1tG9I7CR3+uq3jf7lY3OiE5loHcbsTXFq6Nhjf4tsDNacTkcqmEtsMPawEZI87bUQ/JrHYfubhnMgb89p8FtxvddTOTG8p0K3xCEW5l5cy/7rjuK07xHjThc+Fuql8ODrUnLDrpSPDMoE4oJCNu9lmNuNqcC3bVdkwjHs=^1734930199564; _abck=A70A62194696D36F1AA10D663E1889A1~-1~YAAQD7oXAhCPEsaTAQAA4gfm8Q3fa4T56adNl0bYteBlyD/+vi4HRquJh2FvKSfDMGzbpTIWayPUGr41Ni0mdmw3Qvr6KRjxXJpwrgET5LiU0MdZWeozKMTFCXBp3F5exa3RK6DxZiMaIAxoQlcCZz90Qi6xqb3vzzn0xp6/y4pWMCmV2OrIHmOCAxAur32UxD75cpRiQnncnk7Nz/jafiIwGyNeZBNvtpGppmReaW/38rp4R3QGYu/CVJz3/1d+1nxqi3duuoydhzGKiqAASOduCkMDYN3YP07qKtpDqrL161w1tdILPLczIhBj5lMKHNTdLRgtsQmQmLVHuOAKWZTvBX1SdfYBm7wJOIjOnGOd01o5Qf6sStL7YhDfP2Gp4CCO3k0tPN84zpaPcGBk9jlFZmxWhpP3tLUTUFWqR0rD7/UM5tEXUP0qVINRS2cLMmCL4W8aFR85eseiEwsaviA98nF3vWoQ4ThKSzGaE7NtquL6kTSzNDVmE+OP9UsFqLsdnwlbhxQMgryfFvas5Vdg6l6Uh584DrwqKcRblg==~-1~||0||~-1",
        "origin": "https://store.playstation.com",
        "priority": "u=1, i",
        "referer": "https://store.playstation.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.178 Safari/537.36",
        "x-psn-app-ver": "@sie-ppr-web-store/app/@sie-ppr-web-store/app@0.91.0-7e3c09d0a5db42e73a6287933332fb6478e6c431",
        "x-psn-correlation-id": "e2c7729c-8827-480c-933e-c933539ff80c",
        "x-psn-request-id": "9dad714a-3977-45c0-baef-dfb45b4263e4",
        "x-psn-store-locale-override": "tr-TR",

    }
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



def get_info(
        id: int,
) -> dict:
    """
    :param id:
    :return: {
        basePriceValue: int,
        discountedValue: int,
        endTime: int хранит UNIX time
        name: str,
        type: str (Avaible, Unavaible),
        discont_percent: int

    }
    """
    pass


def get_all_games_ids():
    ans, max_games = get_games_ids()
    for offset in range(1000, max_games, 1000):
        size = 1000
        if max_games - offset < 1000:
            size = max_games - offset
        ans += get_games_ids(
            size=size,
            offset=offset
        )[0]
    return ans





