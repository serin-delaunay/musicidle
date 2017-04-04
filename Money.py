
# coding: utf-8
from typing import List, Tuple, NamedTuple, Optional, Union, Dict, Any
from enum import Enum, auto
from fractions import Fraction

class _DenominationSpec(NamedTuple):
    relative_value : Union[Fraction, int]
    singular : str
    plural : Optional[str] = None
    short : Optional[str] = None

class _Denomination(NamedTuple):
    value : int
    singular : str
    plural : str
    short : str

class Denomination(_Denomination):
    def string(self, abbreviate : bool=False, plural:bool=False) -> str:
        if abbreviate:
            return self.short
        elif plural:
            return self.plural
        else:
            return self.singular

class DenominationSpec(_DenominationSpec):
    def make_denomination(self, previous_denomination : Optional[Denomination] = None) -> Denomination:
        new_value : Fraction
        if previous_denomination is None:
            new_value = Fraction(self.relative_value)
        else:
            new_value = Fraction(previous_denomination.value*self.relative_value)
        assert new_value.denominator == 1
        plural : str = self.singular + 's' if self.plural is None else self.plural
        short : str = ''.join(s[0] for s in self.singular.split()) if self.short is None else self.short
        return Denomination(int(new_value), self.singular.title(), plural.title(), short)

def make_denominations(spec : List[DenominationSpec]) -> List[Denomination]:
    result = []
    result.append(spec[0].make_denomination())
    for ds in spec[1:]:
        result.append(ds.make_denomination(result[-1]))
    return result

# TODO move money specifics into Data.py
_denomination_spec : List[DenominationSpec] = [
    DenominationSpec(1, 'mite'),
    DenominationSpec(6, 'fortress', 'fortresses'),
    DenominationSpec(2, 'happisburgh'),
    DenominationSpec(2, 'pig pen', short='d'),
    DenominationSpec(4, 'goat'),
    DenominationSpec(3, 'seashell', short='/'),
    DenominationSpec(2, 'fioritura', 'fioriture'),
    DenominationSpec(Fraction(5, 2), 'croc'),
    DenominationSpec(4, 'pond', short='£'),
    DenominationSpec(Fraction(21, 20), 'guinea pig'),
    DenominationSpec(Fraction(960,7), 'goose', 'geese', 'gs'),
    DenominationSpec(12, 'great goose', 'great geese')
]

denominations = make_denominations(_denomination_spec)

values : Dict[str,int] = {d.singular : d.value for d in denominations}

class MoneyVerbosity(Enum):
    smallest = 0
    largest = auto()
    top_two = auto()
    full = auto()

class Money(object):
    value : int
    verbosity : MoneyVerbosity
    abbreviate : bool
    def __init__(self,
                 value : int = 0,
                 verbosity : MoneyVerbosity = MoneyVerbosity.full,
                 abbreviate : bool = False) -> None:
        self.value = value
        self.verbosity = verbosity
        self.abbreviate = abbreviate
    def __repr__(self):
        return 'Money({0}, {1}, {2})'.format(self.value, self.verbosity,
                                             'short' if self.abbreviate else 'long')
    def __str__(self):
        # Denominations must be used in this function.
        # How should this function change when data is moved to Data.py?
        space = '' if self.abbreviate else ' '
        if self.verbosity == MoneyVerbosity.smallest:
            return '{0}{1}{2}'.format(self.value,
                                      space,
                                      denominations[0].string(self.abbreviate,
                                                              self.value != 1))
        else:
            units : int = 1
            if self.verbosity == MoneyVerbosity.top_two:
                units = 2
            elif self.verbosity == MoneyVerbosity.full:
                units = len(denominations)
            components : List[str] = []
            remainder : int = self.value
            for count, d in enumerate(reversed(denominations)):
                quotient : int
                quotient, remainder = divmod(remainder, d.value)
                if quotient > 0 or (count == len(denominations)-1 and
                                    len(components) == 0):
                    components.append('{0}{1}{2}'.format(quotient,
                                                         space,
                                                         d.string(self.abbreviate,
                                                                  quotient != 1)))
                    if len(components) >= units:
                        break
            comma_space : str = ' ' if self.abbreviate else ', '
            return comma_space.join(components)

class MoneyContainer(Money):
    capacity : int
    def __init__(self, capacity : int, *args, **kwargs : Dict[str,Any]) -> None:
        super().__init__(*args, **kwargs)
        self.capacity = capacity
    def add(self, value : int) -> None:
        self.value = max(0, min(self.capacity, self.value + value))
    def get_capacity(self) -> Money:
        return Money(self.capacity, self.verbosity, self.abbreviate)
    def __repr__(self) -> str:
        return 'MoneyContainer({0}/{1}, {2}, {3})'.format(
            self.value,
            self.capacity,
            self.verbosity,
            'short' if self.abbreviate else 'long')
    def __str__(self) -> str:
        return '{0} (max {1})'.format(Money.__str__(self),
                                      str(self.get_capacity()))
