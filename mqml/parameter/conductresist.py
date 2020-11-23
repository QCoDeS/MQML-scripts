from qcodes.instrument.parameter import Parameter
from qcodes.instrument.base import Instrument

G_0 = 7.7480917310e-5 #conductance quantum

# Definitions of functions for differential conductance
# and reristance for 2 and 4 probe measurements

class ConductResist(Instrument):
    '''
    This class holds the paramaters for conductance or resistance
    and methods to calculate those based on the parameters generated from lock-ins.

    Args:
        name: The name of a paramater in this class
        lockin_param1: .X value of a lock-in amplifier
        lockin_param2: .X or .amplitude() value of a lock-in amplifier depending on
                        the target parameter
    '''
    def __init__(self, name: str, lockin_param1: Parameter, lockin_param2: Parameter) -> None:
        super().__init__(name)
        self.add_parameter("GIamp",
                            label="Current Amplification",
                            get_cmd=None,
                            set_cmd=None)

        self.add_parameter("GVamp",
                            label="Voltage Amplification",
                            get_cmd=None,
                            set_cmd=None)

        self.add_parameter("ACdiv",
                            label="AC Division",
                            get_cmd=None,
                            set_cmd=None)

        self.add_parameter("DCdiv",
                            label="DC Division",
                            get_cmd=None,
                            set_cmd=None)

        self.add_parameter("diff_conductance_fpm",
                            label="dI/dV",
                            unit='2e^2/h',
                            get_cmd=lambda: self.desoverh_fpm(lockin_param1, lockin_param2)
                            )

        self.add_parameter("conductance_tpm",
                            label="I/V",
                            unit='2e^2/h',
                            get_cmd=lambda: self.desoverh_tpm(lockin_param1, lockin_param2)
                            )

        self.add_parameter("resistance_fpm",
                            label="R",
                            unit='Ohm',
                            get_cmd=lambda: self.ohms_law(lockin_param1, lockin_param2)
                            )

    def desoverh_fpm(self, lockin_param1: Parameter, lockin_param2: Parameter) -> float:
        try:
            return (lockin_param1/self.GIamp())/(lockin_param2/self.GVamp())/G_0
        except ZeroDivisionError as zeroerror:
            print ('No output because the denominator iz zero')
            raise zeroerror
        except TypeError as typerror:
            print('Amplification and/or voltaga divisions are not set. Set them and try again.')
            raise typerror

    def desoverh_tpm(self, lockin_param1: Parameter, lockin_param2: Parameter) -> float:
        try:
            return (lockin_param1/self.GIamp())/(lockin_param2/self.ACdiv())/G_0
        except TypeError as typerror:
            print('Amplification and/or voltaga divisions are not set. Set them and try again.')
            raise typerror

    def ohms_law(self, lockin_param1: Parameter, lockin_param2: Parameter) -> float:
        try:
            return (lockin_param2/self.GVamp())/(lockin_param1/self.GIamp())
        except ZeroDivisionError as zeroerror:
            print ('No output because the denominator iz zero')
            raise zeroerror
        except TypeError as typerror:
            print('Amplification and/or voltaga divisions are not set. Set them and try again.')
            raise typerror
