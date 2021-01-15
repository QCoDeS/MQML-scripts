"""The test file for conductresist.py"""
import pytest
from mqml.instrument.conductresist import ConductResist
from qcodes.instrument.base import Instrument
from qcodes.instrument.parameter import Parameter
import numpy as np
import warnings

@pytest.fixture(autouse=True)
def close_all_instruments():
    """Makes sure that after startup and teardown, all instruments are closed"""
    Instrument.close_all()
    yield
    Instrument.close_all()

def test_get_initial_values():
    "This tests the initial values of non-calculated parameters in the class"
    volt1 = Parameter('volt1', set_cmd=None)
    volt2 = Parameter('volt2', set_cmd=None)
    amp = Parameter('amp', set_cmd=None)
    test_inst = ConductResist('test_inst', lockin1_volt=volt1, lockin2_volt=volt2, lockin1_amp=amp)

    assert test_inst.GIamp() == None
    assert test_inst.GVamp() == None
    assert test_inst.ACdiv() == 1e-4
    assert test_inst.DCdiv() == 1e-2

def test_errors():
    "This tests the erros"
    volt1 = Parameter('volt1', set_cmd=None)
    volt2 = Parameter('volt2', set_cmd=None)
    amp = Parameter('amp', set_cmd=None)
    test_inst = ConductResist('test_inst', lockin1_volt=volt1, lockin2_volt=volt2, lockin1_amp=amp)

    with pytest.raises(TypeError, match="(\'Amplification and/or voltage divisions are not set. Set "\
                            "them and try again.\', \'getting test_inst_diff_conductance_fpm\')"):
        test_inst.diff_conductance_fpm()

    with pytest.raises(TypeError, match="(\'Amplification and/or voltage divisions are not set. Set "\
                            "them and try again.\', \'getting test_inst_conductance_tpm\')"):
        test_inst.conductance_tpm()

    with pytest.raises(TypeError, match="(\'Amplification and/or voltage divisions are not set. Set "\
                            "them and try again.\', \'getting test_inst_resistance_fpm\')"):
        test_inst.resistance_fpm()

def test_warnings():
    "This tests warnings if zero divisions occur"
    volt1 = Parameter('volt1', set_cmd=None, initial_value=1.)
    volt2 = Parameter('volt2', set_cmd=None, initial_value=0.)
    amp = Parameter('amp', set_cmd=None, initial_value=0.)
    test_inst = ConductResist('test_inst', lockin1_volt=volt1, lockin2_volt=volt2, lockin1_amp=amp)
    test_inst.GIamp(1e7)
    test_inst.GVamp(100.)

    with pytest.warns(UserWarning, match='The denominator is zero, returning NaN'):
        assert test_inst.diff_conductance_fpm() is np.nan
        assert test_inst.conductance_tpm() is np.nan

    volt1 = Parameter('volt1', set_cmd=None, initial_value=0.)
    volt2 = Parameter('volt2', set_cmd=None, initial_value=1.)
    amp = Parameter('amp', set_cmd=None)
    test_inst2 = ConductResist('test_inst2', lockin1_volt=volt1, lockin2_volt=volt2, lockin1_amp=amp)
    test_inst2.GIamp(1e7)
    test_inst2.GVamp(100.)

    with pytest.warns(UserWarning, match='The denominator is zero, returning NaN'):
        assert test_inst2.resistance_fpm() is np.nan

def test_returning_correct_values():
    "This tests the returned values of the class for calculated parameters"
    volt1 = Parameter('volt1', set_cmd=None, initial_value=1.)
    volt2 = Parameter('volt2', set_cmd=None, initial_value=2.)
    amp = Parameter('amp', set_cmd=None, initial_value=3.)
    test_inst = ConductResist('test_inst', lockin1_volt=volt1, lockin2_volt=volt2, lockin1_amp=amp)
    test_inst.GIamp(1e7)
    test_inst.GVamp(100.)

    # ACDiv value is its initial value.
    assert test_inst.diff_conductance_fpm() == 0.06453201863879687
    assert test_inst.conductance_tpm() == 4.3021345759197915
    assert test_inst.resistance_fpm() == 200000.0
