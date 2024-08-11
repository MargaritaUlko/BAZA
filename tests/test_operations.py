from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/operations", json={
        "id": 3,
        "quantity": "string",
        "figi": "figi_CODE",
        "date": "2024-07-18 01:50:41.604",
        "type": "Выплата купонов",
    }, follow_redirects=True)

    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.text}")

    assert response.status_code == 200


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/operations", params={
        "operation_type": "hui",
    }, follow_redirects=True)

    print(f"Status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.text}")

    assert response.status_code == 200
