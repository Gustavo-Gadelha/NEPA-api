def test_app_exists(app):
    assert app is not None


def test_app_creation():
    from app import create_app
    app = create_app('testing')
    assert app.testing is True
