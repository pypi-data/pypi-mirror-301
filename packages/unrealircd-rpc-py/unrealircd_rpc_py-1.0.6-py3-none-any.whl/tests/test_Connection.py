from unrealircd_rpc_py.Loader import Loader

def test_wrong_link():
    """## Wrong link
    """
    rpc = Loader(
                req_method='socket',
                url='https://deb.biz.st:8600/ap2i',
                username='readonly',
                password='uT9!x7GzV1#sDk3bL5wP@8YrX&f6mQa',
                debug_level=10
            )

    assert rpc.Error.code == -1

def test_invalid_auth_socket():
    """### Authentication failed with Socket
    """
    rpc = Loader(
                req_method='socket',
                url='https://deb.biz.st:8600/api',
                username='readonly1',
                password='uT9!x7GzV1#sDk3bL5wP@8YrX&f6mQa',
                debug_level=10
            )

    assert rpc.Error.code == -1
    assert rpc.Error.message == '>> Authentication required <<'

def test_invalid_auth_requests():
    """## Authentication failed with requests
    """
    rpc = Loader(
                req_method='requests',
                url='https://deb.biz.st:8600/api',
                username='readonly1',
                password='uT9!x7GzV1#sDk3bL5wP@8YrX&f6mQa',
                debug_level=10
            )

    assert rpc.Error.code == -1
    assert rpc.Error.message == '>> Authentication required <<' or ">> Connection Aborted <<"

def test_invalid_method():
    """## Invalid method
    """
    test_rpc = Loader(
                req_method='mynewmethod',
                url='https://deb.biz.st:8600/api',
                username='readonly1',
                password='uT9!x7GzV1#sDk3bL5wP@8YrX&f6mQa',
                debug_level=10
            )

    assert test_rpc.Error.code == -1
    assert test_rpc.Error.message == '<< Invalid method >>'