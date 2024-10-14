from unrealircd_rpc_py.Loader import Loader
import unrealircd_rpc_py.Definition as dfn

rpc = Loader(
                req_method='socket',
                url='https://deb.biz.st:8600/api',
                username='adminpanel',
                password='25T@bler@ne',
                debug_level=10
            )

nickname_for_get_user = 'adator'

nickname = 'adator_test'
nickname_new = 'rpc_test'
username = 'rpc_test'

nickname_not_available = 'xxxxxxx'


def test_get_user():
    """Get a user adator"""

    UserObj = rpc.User

    get_user = UserObj.get(nickname_for_get_user)
    assert get_user.name == nickname_for_get_user

    get_user = UserObj.get('adator11')
    assert get_user == None
    assert UserObj.Error.message == 'Nickname not found'

def test_list_users():
    """Get a user adator"""

    UserObj = rpc.User

    for i in range(1, 4):
        list_user = UserObj.list_(i)
        assert type(list_user) == list

    list_user = UserObj.list_(3)
    assert UserObj.Error.code == -32602

def test_set_nick():
    """Get a user adator"""

    UserObj = rpc.User

    set_nick = UserObj.set_nick(nickname, nickname_new, True)
    assert set_nick == True

    set_nick = UserObj.set_nick(nickname_not_available, 'adator_test', True)
    assert set_nick == False

    set_nick = UserObj.set_nick(nickname_new, nickname, True)
    assert set_nick == True

def test_set_username():
    """Get a user adator"""

    UserObj = rpc.User

    set_nick = UserObj.set_username(nickname, username)
    assert type(set_nick) == bool
    
    if not set_nick:
        assert UserObj.Error.code != 0

    set_nick = UserObj.set_username(nickname_not_available, 'adator_test')
    assert set_nick == False

def test_set_realname():
    """Set realname"""

    UserObj = rpc.User

    set_nick = UserObj.set_realname('adator_test', 'jrpc_test')
    assert type(set_nick) == bool

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

    set_nick = UserObj.set_realname('xxxxxx', 'adator_test')
    assert set_nick == False

def test_set_vhost():
    """Set realname"""

    UserObj = rpc.User

    set_nick = UserObj.set_vhost('adator_test', 'jsonrpc.deb.biz.st')
    assert type(set_nick) == bool

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

    set_nick = UserObj.set_vhost('xxxxxx', 'jsonrpc.deb.biz.st')
    assert set_nick == False

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

def test_set_mode():
    """Set realname"""

    UserObj = rpc.User

    set_nick = UserObj.set_mode('adator_test', '-o')
    assert type(set_nick) == bool

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

    UserObj.set_mode('adator_test', '+t')

    set_nick = UserObj.set_mode('xxxxxx', 'jsonrpc.deb.biz.st')
    assert set_nick == False

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

def test_set_snomask():
    """Set snomask"""

    UserObj = rpc.User

    set_nick = UserObj.set_snomask(nickname, '+s')
    assert type(set_nick) == bool

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

    UserObj.set_snomask(nickname, '-s')

    set_nick = UserObj.set_snomask(nickname_not_available, '+x')
    assert set_nick == False

    if not set_nick:
        assert UserObj.Error != 0
        print( UserObj.Error.code, UserObj.Error.message, sep=' --> ')

def test_set_oper():
    """Set oper"""

    UserObj = rpc.User

    set_oper = UserObj.set_oper(nickname, 'adator', 'adator')
    print(UserObj.Error.code)
    if UserObj.Error.code != 0:
        assert set_oper == True
