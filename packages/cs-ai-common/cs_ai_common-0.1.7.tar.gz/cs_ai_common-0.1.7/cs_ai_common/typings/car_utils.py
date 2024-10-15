from enum import StrEnum

_TRANSMISIONS_AUTO = ['automatic', 'automatic_transmission', 'automatyczna']
_TRANSMISIONS_MANUAL = ['manual', 'manual_transmission', 'manualna']

class Transmisions(StrEnum):
    AUTO = 'automatic'
    MANUAL = 'manual'

    @staticmethod
    def to_common(value: str) -> 'Transmisions':
        value = value.lower()
        if value in _TRANSMISIONS_MANUAL:
            return Transmisions.MANUAL
        
        if value in _TRANSMISIONS_AUTO:
            return Transmisions.AUTO
        
        raise ValueError(f'Invalid value: {value}')


class FuelTypes(StrEnum):
    PETROL = 'petrol'
    PETROL_CNG = 'petrol_cng'
    PETROL_LPG = 'petrol_lpg'
    DIESEL = 'diesel'
    ELECTRIC = 'electric'
    ETHANOL = 'ethanol'
    HYBRID = 'hybrid'
    PLUGIN_HYBRID = 'plugin_hybrid'
    HYDROGEN = 'hydrogen'

    @staticmethod
    def to_common(value: str) -> 'FuelTypes':
        value = value.lower().replace('-', '_')
        enum_value = FuelTypes.__members__.get(value.upper())

        if enum_value:
            return enum_value

        raise ValueError(f'Invalid value: {value}')
    