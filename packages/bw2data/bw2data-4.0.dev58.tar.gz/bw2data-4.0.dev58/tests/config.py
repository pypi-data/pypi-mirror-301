from bw2data import config
from bw2data.tests import bw2test


@bw2test
def test_default_biosphere():
    assert config.biosphere == "biosphere3"


@bw2test
def test_default_geo():
    assert config.global_location == "GLO"
