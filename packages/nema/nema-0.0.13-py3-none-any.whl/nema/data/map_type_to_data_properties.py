from nema.data.data_type import DataType
from nema.data.data_properties import (
    StringValue,
    IntegerValue,
    FloatValue,
    CurrencyValue,
    FloatValueWithArbitraryUnit,
    IntValueWithArbitraryUnit,
    FloatValueWithPhysicalUnit,
    IntValueWithPhysicalUnit,
)


def map_type_to_data_properties(data_type: DataType):
    if data_type == DataType.STRING:
        return StringValue
    elif data_type == DataType.INT:
        return IntegerValue
    elif data_type == DataType.FLOAT:
        return FloatValue
    elif data_type == DataType.CURRENCY:
        return CurrencyValue
    elif data_type == DataType.FLOAT_WITH_ARBITRARY_UNIT_V0:
        return FloatValueWithArbitraryUnit
    elif data_type == DataType.INT_WITH_ARBITRARY_UNIT_V0:
        return IntValueWithArbitraryUnit
    elif data_type == DataType.FLOAT_WITH_PHYSICAL_UNIT_V0:
        return FloatValueWithPhysicalUnit
    elif data_type == DataType.INT_WITH_PHYSICAL_UNIT_V0:
        return IntValueWithPhysicalUnit
    else:
        raise ValueError(f"Data type {data_type} not supported.")
