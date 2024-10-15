from click.testing import CliRunner
from murmuration.kms_wrapped import encrypt
from waddle.param_bunch import ParamBunch
from waddle import cli
from waddle.yaml_base import KmsWrappedSecret


def test_load(master_keyed_conf):
    """
    can we load and decrypt a file with a master-keyed secret?
    """
    conf = master_keyed_conf
    assert conf.good.cat == 'mr. whiskers'
    assert conf.good.dogs[0] == 'peanut'
    assert conf.good.dogs[1] == 'gwenna'


def test_to_dict(master_keyed_conf):
    """
    can we serialize a master keyed config file to a dict?
    """
    conf = master_keyed_conf.to_dict()
    assert conf['good']['cat'] == 'mr. whiskers'
    assert conf['good']['dogs'][0] == 'peanut'
    assert conf['good']['dogs'][1] == 'gwenna'


def test_add_secret(temp_master_keyed_filename):
    secret = 'salu'
    filename = temp_master_keyed_filename
    runner = CliRunner()
    runner.invoke(
        cli.main, [
            'add-secret',
            '-f',
            filename,
            'good.porcupine',
        ], input=f'{secret}\n')
    with open(filename, 'r') as f:
        contents = f.read()
    assert 'porcupine: !secret' in contents
    b = ParamBunch()
    b.load(filename=filename)
    assert b.good.porcupine == secret


def test_with_role_arn(temp_master_keyed_filename, role_arn):
    filename = temp_master_keyed_filename
    b = ParamBunch(filename=filename)
    b.meta.role_arn = role_arn
    master_key = b.meta.master_key
    kms_key = b.meta.kms_key
    profile = b.meta.profile
    encrypted_master_key = encrypt(
        master_key, profile=profile, alias=kms_key, role_arn=role_arn)
    b.meta.master_key = KmsWrappedSecret(encrypted_master_key)
    b.save(filename)
    conf = ParamBunch(filename=filename)
    assert conf.good.cat == 'mr. whiskers'
    assert conf.good.dogs[0] == 'peanut'
