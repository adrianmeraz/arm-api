import respx
import httpx

def mock_route(method: str, data: dict) -> respx.Route:
    route = respx.route(
        method=method,
    ).mock(
        return_value=httpx.Response(
            headers=None,
            status_code=200,
            json=data,
        )
    )