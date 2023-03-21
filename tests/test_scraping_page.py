from tests.utils import register, login


def test_download(client):
    response = client.get("/scraping")
    assert response.status_code == 302

    register("sam")
    login(client, "sam")

    response = client.get("/scraping")
    assert response.status_code == 200
    assert b"Logout" in response.data
    assert b"Search Real Estate Sites" in response.data
    assert b"Download" in response.data
