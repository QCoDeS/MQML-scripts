import pytest

from mqml.parameter.conductresist import ConductResist
from qcodes.instrument.base import Instrument
import numpy as np

@pytest.fixture(autouse=True)
def close_all_instruments():
    """Makes sure that after startup and teardown all instruments are closed"""
    Instrument.close_all()
    yield
    Instrument.close_all()

def test_get_static_parameters():
    "This tests the initial values of static parameters in the class"
    lockin_param1 = 1
    lockin_param2 = 2
    test_param = ConductResist('test_param', lockin_param1=lockin_param1, lockin_param2=lockin_param2)

    assert test_param.GIamp() == None
    assert test_param.GVamp() == None
    assert test_param.ACdiv() == 1e-4
    assert test_param.DCdiv() == 1e-2

def test_errors():
    "This tests the erros"
    lockin_param1 = 1
    lockin_param2 = 2
    test_param = ConductResist('test_param', lockin_param1=lockin_param1, lockin_param2=lockin_param2)

    with pytest.raises(TypeError) as e:
        test_param.diff_conductance_fpm()
    assert str(e.value) == "(\'Amplification and/or voltage divisions are not set. Set them and try again.\', \'getting "\
                            "test_param_diff_conductance_fpm\')"

    with pytest.raises(TypeError) as e:
        test_param.conductance_tpm()
    assert str(e.value) == "(\'Amplification and/or voltage divisions are not set. Set them and try again.\', \'getting "\
                            "test_param_conductance_tpm\')"

    with pytest.raises(TypeError) as e:
        test_param.resistance_fpm()
    assert str(e.value) == "(\'Amplification and/or voltage divisions are not set. Set them and try again.\', \'getting "\
                            "test_param_resistance_fpm\')"

def test_warnings():
    "This tests warnings if zero divisions occur"
    lockin_param1 = 1.0
    lockin_param2 = 0.0
    test_param = ConductResist('test_param', lockin_param1=lockin_param1, lockin_param2=lockin_param2)
    test_param.GIamp(1e7)
    test_param.GVamp(100.0)
    nan = np.nan

    assert test_param.diff_conductance_fpm() is nan
    assert test_param.conductance_tpm() is nan

    lockin_param1 = 0.0
    lockin_param2 = 1.0
    test_param2 = ConductResist('test_param2', lockin_param1=lockin_param1, lockin_param2=lockin_param2)
    test_param2.GIamp(1e7)
    test_param2.GVamp(100.0)

    assert test_param2.resistance_fpm() is nan

def test_returning_correct_values():
    "This tests the returned values of the class for calculated parameters"
    lockin_param1 = 1.0
    lockin_param2 = 2.0
    test_param = ConductResist('test_param', lockin_param1=lockin_param1, lockin_param2=lockin_param2)
    test_param.GIamp(1e7)
    test_param.GVamp(100.0)

    # ACDiv value is its initial value.

    assert test_param.diff_conductance_fpm() == 0.06453201863879687

    assert test_param.conductance_tpm() == 6.453201863879687

    assert test_param.resistance_fpm() == 200000.0
