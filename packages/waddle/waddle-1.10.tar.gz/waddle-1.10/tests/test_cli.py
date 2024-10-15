import os
from shutil import copyfile
import time
from unittest import TestCase
import pytest
from click.testing import CliRunner
from waddle import cli
from waddle.param_bunch import ParamBunch
from waddle.aws import yield_parameters
from waddle.yaml_base import KmsWrappedSecret


class TestCli(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        self.caplog = caplog

    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ['--version'])
        self.assertIn('waddle', result.output)

    def test_add_key(self):
        filename = 'tests/conf/secret.yml'
        copyfile('tests/conf/nested.yml', filename)
        self.add_secret(filename)
        self.add_secret_in_place(filename)
        self.add_secret_failure()
        os.remove(filename)

    def test_comment_preservation(self):
        filename = 'tests/conf/add_key.yml'
        copyfile('tests/conf/add_key.input.yml', filename)
        b = ParamBunch()
        b.load(filename=filename, round_trip=True)
        b.waddle.preferred = 'cats'
        b.save(filename=filename)
        with open(filename, 'r') as f:
            data = f.read()
        self.assertIn('# these are the development dogs', data)
        self.assertIn('# these are the development cats', data)
        os.remove(filename)

    def add_secret(self, filename):
        secret = 'this is super secret'
        runner = CliRunner()
        runner.invoke(
            cli.main, [
                'add-secret',
                '-f',
                filename,
                'waddle.secret',
            ], input=f'{secret}\n')

        b = ParamBunch()
        b.load(filename=filename)
        self.assertIn('cody', b.waddle.cats)
        self.assertEqual(b.waddle.preferred, 'cats')
        value = b.waddle.secret
        self.assertEqual(value, secret)
        self.assertIn('waddle.secret', b.encrypted)

    def add_secret_in_place(self, filename):
        runner = CliRunner()
        runner.invoke(
            cli.main, [
                'add-secret',
                '-i',
                '-f',
                filename,
                'waddle.preferred',
            ])

        b = ParamBunch()
        b.load(filename=filename)
        self.assertEqual(b.waddle.preferred, 'cats')

    def has_log(self, message):
        for x in self.caplog.messages:
            if message in x:
                return True
        return False

    def add_secret_failure(self):
        runner = CliRunner()
        runner.invoke(
            cli.main, [
                'add-secret',
                '-f',
                'tests/conf/encrypted.yml',
                'waddle.secret',
            ], input='whatwhat\n')
        assert self.has_log('needs one of kms_key or master_key')

    def test_is_secret(self):
        self.assertTrue(cli.is_secret('some.secret'))
        self.assertTrue(cli.is_secret('some.password'))
        self.assertFalse(cli.is_secret('some.username'))
        self.assertTrue(cli.is_secret('some.api_key'))
        self.assertTrue(cli.is_secret('some.oauth_token'))

    def test_encrypt(self):
        filename = 'tests/conf/test.yml'
        copyfile('tests/conf/cli-encrypt.yml', filename)
        runner = CliRunner()
        runner.invoke(
            cli.main, [
                'encrypt',
                '-f',
                filename,
            ])
        x = ParamBunch()
        x.load(filename=filename, decrypt=False)
        _, _, value = x.original_value('waddle.db.password')
        self.assertIsInstance(value, KmsWrappedSecret)
        _, _, value = x.original_value('waddle.api.token')
        self.assertIsInstance(value, KmsWrappedSecret)
        self.assertEqual(x.waddle.public, 'jinx')
        _, _, value = x.original_value('oauth.token')
        self.assertIsInstance(value, KmsWrappedSecret)
        _, _, value = x.original_value('waddle.secret.favorite_dog')
        self.assertIsInstance(value, KmsWrappedSecret)
        os.remove(filename)

    def test_encrypt_failure(self):
        runner = CliRunner()
        runner.invoke(
            cli.main, [
                'encrypt',
                '-f',
                'tests/conf/encrypted.yml',
            ], input='whatwhat\n')
        assert self.has_log('needs one of kms_key or master_key')

    def test_deploy(self):
        runner = CliRunner()
        filename = 'tests/conf/deploy.yml'
        runner.invoke(
            cli.main,
            [ 'deploy', '-f', filename, ])
        time.sleep(5)
        conf = ParamBunch(prefix='/test')
        self.assertEqual(conf.waddle.cat, 'stella')
        self.assertEqual(conf.waddle.dog, 'olive')

        runner.invoke(
            cli.main,
            [ 'undeploy', '-f', filename, ])
        deleted_keys = [ '/test/waddle/cat', '/test/waddle/dog', ]
        time.sleep(5)
        for key in yield_parameters('/test'):
            self.assertNotIn(key, deleted_keys)


def test_add_master_key(temp_blank_config):
    """
    can we add a master key to a blank config file
    """
    runner = CliRunner()
    filename = temp_blank_config
    runner.invoke(
        cli.main,
        ['add-master-key', '-f', filename, ])
    conf = ParamBunch(filename=temp_blank_config)
    master_key = conf.meta.master_key
    assert master_key is not None
    secret = 'this is super secret'
    runner = CliRunner()
    runner.invoke(
        cli.main, [
            'add-secret',
            '-f',
            filename,
            'waddle.secret',
        ], input=f'{secret}\n')
    conf = ParamBunch(filename=temp_blank_config)
    assert conf.waddle.secret == secret
    runner.invoke(
        cli.main,
        ['add-master-key', '-f', filename, ])
    conf = ParamBunch(filename=temp_blank_config)
    assert conf.waddle.secret == secret
    assert conf.meta.master_key != master_key
