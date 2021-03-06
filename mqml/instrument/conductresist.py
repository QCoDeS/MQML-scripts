""" Definition of an instrument to calculate differential conductance and reristance for 2 and 4 probe
measurements using inputs of two lock-in amplifiers"""

from qcodes.instrument.parameter import Parameter
from qcodes.instrument.base import Instrument
import numpy as np
import warnings

G_0 = 7.7480917310e-5 #conductance quantum

class ConductResist(Instrument):
    """
    This class holds conductance and resistance parameters, which are calculated using voltage and amplitude
    parameters generated by two lock-in amplifiers. Current and voltage amplifications and/ or divisions are
    also set in the class.

    Args:
        name: the name of a created instrument
        lockin1_volt: X parameter of the first lock-in, e.g., Lockin1.X
        lockin1_amp: amplitude parameter of the first lock-in, e.g., Lockin1.amplitude
        lockin2_volt: X parameter of the second lock-in, e.g., Lockin2.X
    """
    def __init__(self, name: str, *, lockin1_volt: Parameter, lockin1_amp: Parameter, lockin2_volt: Parameter) -> None:
        super().__init__(name)
        self._lockin1_volt = lockin1_volt
        self._lockin2_volt = lockin2_volt
        self._lockin1_amp = lockin1_amp

        self.add_parameter("GIamp",
                            label="Current Amplification",
                            get_cmd=None,
                            set_cmd=None
                            )

        self.add_parameter("GVamp",
                            label="Voltage Amplification",
                            get_cmd=None,
                            set_cmd=None
                            )

        self.add_parameter("ACdiv",
                            label="AC Division",
                            get_cmd=None,
                            set_cmd=None,
                            initial_value=1e-4
                            )

        self.add_parameter("DCdiv",
                            label="DC Division",
                            get_cmd=None,
                            set_cmd=None,
                            initial_value=1e-2
                            )

        self.add_parameter("diff_conductance_fpm",
                            label="dI/dV",
                            unit='2e^2/h',
                            get_cmd=self._desoverh_fpm
                            )

        self.add_parameter("conductance_tpm",
                            label="I/V",
                            unit='2e^2/h',
                            get_cmd=self._desoverh_tpm
                            )

        self.add_parameter("resistance_fpm",
                            label="R",
                            unit='Ohm',
                            get_cmd=self._ohms_law
                            )

    def _desoverh_fpm(self) -> float:
        try:
            return (self._lockin1_volt()/self.GIamp())/(self._lockin2_volt()/self.GVamp())/G_0
        except ZeroDivisionError:
            warnings.warn('The denominator is zero, returning NaN')
            return np.nan
        except TypeError:
            raise TypeError('Amplification and/or voltage divisions are not set. Set them and try again.')

    def _desoverh_tpm(self) -> float:
        try:
            return (self._lockin1_volt()/self.GIamp())/(self._lockin1_amp()*self.ACdiv())/G_0
        except ZeroDivisionError:
            warnings.warn('The denominator is zero, returning NaN')
            return np.nan
        except TypeError:
            raise TypeError('Amplification and/or voltage divisions are not set. Set them and try again.')

    def _ohms_law(self) -> float:
        try:
            return (self._lockin2_volt()/self.GVamp())/(self._lockin1_volt()/self.GIamp())
        except ZeroDivisionError:
            warnings.warn('The denominator is zero, returning NaN')
            return np.nan
        except TypeError:
            raise TypeError('Amplification and/or voltage divisions are not set. Set them and try again.')
