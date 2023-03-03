import types

from app.google_package.base import GoogleBaseClient

try:
    from app.google_package import base
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен файл `base.py`. '
        'Проверьте и поправьте: он должн быть доступен в директории `app/google_package/`.',
    )


def test_google_base_client():
    assert hasattr(base, 'GoogleBaseClient'), (
        'В файле `base.py` не обнаружен класс `GoogleBaseClient`'
    )


def test_scopes():
    assert hasattr(GoogleBaseClient, 'SCOPES'), (
        'В классе `GoogleBaseClient` не обнаружена переменная `SCOPES`'
    )
    assert len(GoogleBaseClient.SCOPES) == 2, (
        'Убедитесь что количество объектов в `GoogleBaseClient.SCOPES` равно двум.'
    )
    for scope in GoogleBaseClient.SCOPES:
        assert any(s in scope for s in ['drive', 'spreadsheets']), (
            'В `GoogleBaseClient.SCOPES` не обнаружен необходимый уровень доступа'
        )


def test_info():
    assert hasattr(GoogleBaseClient, 'INFO'), (
        'В классе `GoogleBaseClient` не обнаружена переменная `INFO`'
    )
    for info_key in (  # needed_keys
        'type',
        'project_id',
        'private_key_id',
        'private_key',
        'client_email',
        'client_id',
        'auth_uri',
        'token_uri',
        'auth_provider_x509_cert_url',
        'client_x509_cert_url',
    ):
        assert info_key in GoogleBaseClient.INFO, (
            f'В объекте `GoogleBaseClient.INFO` не обнаружено ключа `{info_key}`'
        )


def test_connect():
    assert hasattr(GoogleBaseClient, 'get_google_service'), (
        'В классе `GoogleBaseClient` не обнаружена функция `get_google_service`'
    )
    assert isinstance(GoogleBaseClient().get_google_service(), types.AsyncGeneratorType), (
        'Функция `GoogleBaseClient.get_google_service` должна возвращать асинхронный генератор.'
    )
