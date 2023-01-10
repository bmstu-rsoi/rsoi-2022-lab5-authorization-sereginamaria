import requests
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class Response:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class Request:
    def __init__(
        self,
        /, *,
        method: str,
        url: str,
        headers: dict[str, str],
        params: dict[str, int | float | str],
        data: dict,
        instance,
    ):
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self.data = data
        self.instance = instance

    def __repr__(self):
        return f"<{self.__class__.__name__}: ({self.method}, {self.url}, {self.headers}, {self.params}, {self.data}>"

    def execute(self):
        if OAuth2Authentication().authenticate(self.instance) is None:
            return Response(status_code=401)
        headers = {k: v for k, v in self.headers.items()}
        headers["Authorization"] = self.instance.user.username
        try:
            return requests.request(
                method=self.method,
                url=self.url,
                headers=headers,
                params=self.params,
                data=self.data,
            )
        except requests.exceptions.ConnectionError as ex:
            return Response(status_code=503)

