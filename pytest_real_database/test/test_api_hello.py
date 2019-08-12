from quote_app import Quote


def test_api_hello__no_quote(api_client):
    resp = api_client.get('/api/hello')
    assert resp.status_code == 200
    assert resp.json['message'] == 'hello, world'


def test_api_hello__single_quote(db, api_client):
    quote = Quote()
    quote.mesage = 'test-mesage'
    db.session.add(quote)
    db.session.commit()

    resp = api_client.get('/api/hello')
    assert resp.status_code == 200
    assert resp.json['message'] == quote.message
