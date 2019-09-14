from .factory import QuoteFactory


def test_create_one_quote(db):
    quote = QuoteFactory.create()
    db.session.commit()
    assert quote.id is not None
    assert quote.author
    assert quote.message


def test_create_many_quotes(db):
    expected_author = 'Louis Armstrong'
    quotes = QuoteFactory.create_batch(100, author=expected_author)
    db.session.commit()
    for quote in quotes:
        assert quote.id is not None
        assert quote.author == expected_author
        assert quote.message
