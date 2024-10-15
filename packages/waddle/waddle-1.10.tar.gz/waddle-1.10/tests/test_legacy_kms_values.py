from waddle.param_bunch import ParamBunch


def test_load(legacy_kms_values_filename):
    """
    can we decrypt untagged kms-wrapped secrets?
    """
    conf = ParamBunch(filename=legacy_kms_values_filename)
    assert conf.favorite_dog == 'gwenna'
    assert conf.nonsense_value == 'AQI_nonsense_value'
