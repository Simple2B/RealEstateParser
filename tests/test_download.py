from tests.utils import register, login


def test_download(client):
    response = client.get("/download")
    assert response.status_code == 302

    register("sam")
    login(client, "sam")

    response = client.get("/download")
    assert response.status_code == 200
    assert response.content_type == "text/csv; charset=utf-8"
    assert b"URL,Emails,Phones" in response.data
