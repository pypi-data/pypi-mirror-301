from typing import Optional, Final

import aiohttp

from instagram_direct.direct_api.client import BASE_URL


class Client:

    _HEADERS: Final[dict] = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        "x-ig-app-id": "1217981644879628"
    }

    def __init__(self, session_id: str):
        self._cookies = {
            "sessionid": session_id
        }

    async def get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=BASE_URL + endpoint,
                    params=params,
                    cookies=self._cookies,
                    headers=self._HEADERS,
                    ssl=False
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception("")

    def post(self): ...
