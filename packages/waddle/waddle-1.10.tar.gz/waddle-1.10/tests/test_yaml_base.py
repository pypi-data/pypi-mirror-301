from functools import partial
from yaml import SafeLoader, load
from waddle.yaml_base import load_yaml_basic
from waddle.yaml_base import KmsWrappedSecret
from waddle.yaml_base import MasterKeyedSecret
from waddle.yaml_base import master_keyed_scalar_constructor
from waddle.yaml_base import ssm_scalar_constructor
from waddle.yaml_base import kms_wrapped_scalar_constructor


def test_load_yaml_basic(master_keyed_filename):
    """
    can we use the basic waddle loader?
    """
    data, master_key, special_values = load_yaml_basic(master_keyed_filename)
    assert isinstance(master_key, KmsWrappedSecret)
    secret = data['good']['dogs'][0]
    assert isinstance(secret, MasterKeyedSecret)
    assert secret.master_key == master_key
    assert data['good']['dogs'][0] in special_values


def test_no_special_values(master_keyed_filename):
    """
    will our yaml constructors work when special_values is None?
    """
    class WaddleLoader(SafeLoader):
        pass

    ssm_fn = partial(ssm_scalar_constructor)
    kms_wrapped_fn = partial(kms_wrapped_scalar_constructor)
    master_keyed_wrapped_fn = partial(master_keyed_scalar_constructor)
    WaddleLoader.add_constructor('!secret', master_keyed_wrapped_fn)
    WaddleLoader.add_constructor('!ssm', ssm_fn)
    WaddleLoader.add_constructor('!kms_wrapped', kms_wrapped_fn)

    with open(master_keyed_filename, 'r') as f:
        data = load(f, Loader=WaddleLoader)
    master_key = data.get('meta', {}).get('master_key')
    assert isinstance(master_key, KmsWrappedSecret)
