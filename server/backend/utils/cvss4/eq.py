# Copyright 2023 binsec systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from decimal import Decimal
from typing import Generator

from .maps import SCORE_MAP
from .vector import CVSS4Vector


class _EQ:
    vector_keys: list[str] = []
    _maxes: dict[int, list[str]] = {}
    _severity: dict[int, int] = {}

    def __init__(self, vector: CVSS4Vector) -> None:
        self._vector = vector
        self._values = vector.asdict(self.vector_keys)

    def __str__(self) -> str:
        return str(self.value)

    @property
    def value(self) -> int:
        raise NotImplementedError()

    @property
    def maxes(self) -> list[str]:
        return self._maxes[self.value]

    @property
    def max_severity(self) -> Decimal:
        return self._severity[self.value] * Decimal('0.1')

    def _fvalues(self, keys: list[str]) -> dict[str, str]:
        return {x[0]: x[1] for x in self._values.items() if x[0] in keys}


class EQ1(_EQ):
    """
    EQ1 reprecentation for CVSS4

    See: see table 24 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    vector_keys = ['AV', 'PR', 'UI']
    _maxes = {
        0: ['AV:N/PR:N/UI:N/'],
        1: ['AV:A/PR:N/UI:N/', 'AV:N/PR:L/UI:N/', 'AV:N/PR:N/UI:P/'],
        2: ['AV:P/PR:N/UI:N/', 'AV:A/PR:L/UI:P/'],
    }
    _severity = {
        0: 1,
        1: 4,
        2: 5,
    }

    @property
    def value(self) -> int:
        if all(x == 'N' for x in self._values.values()):
            return 0
        if (any(x == 'N' for x in self._values.values())
                and self._values['AV'] != 'P'):
            return 1
        return 2


class EQ2(_EQ):
    """
    EQ2 reprecentation for CVSS4

    See: see table 25 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    vector_keys = ['AC', 'AT']
    _maxes = {
        0: ['AC:L/AT:N/'],
        1: ['AC:H/AT:N/', 'AC:L/AT:P/'],
    }
    _severity = {
        0: 1,
        1: 2,
    }

    @property
    def value(self) -> int:
        if self._values['AC'] == 'L' and self._values['AT'] == 'N':
            return 0
        return 1


class EQ3(_EQ):
    """
    EQ3 reprecentation for CVSS4

    See: see table 26 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    vector_keys = ['VC', 'VI', 'VH']

    @property
    def value(self) -> int:
        if all(x == 'H' for x in self._fvalues(['VC', 'VI']).values()):
            return 0
        if any(x == 'H' for x in self._values.values()):
            return 1
        return 2

    @property
    def maxes(self) -> None:
        raise TypeError('Use EQ3EQ6 for maxes')

    @property
    def max_severity(self) -> None:
        raise TypeError('Use EQ3EQ6 for max_severity')


class EQ4(_EQ):
    """
    EQ4 reprecentation for CVSS4

    See: see table 27 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    vector_keys = ['MSI', 'MSA', 'SC', 'SI', 'SA']
    _maxes = {
        0: ['SC:H/SI:S/SA:S/'],
        1: ['SC:H/SI:H/SA:H/'],
        2: ['SC:L/SI:L/SA:L/'],
    }
    _severity = {
        0: 6,
        1: 5,
        2: 4,
    }

    @property
    def value(self) -> int:
        if any(x == 'S' for x in self._fvalues(['MSI', 'MSA']).values()):
            return 0
        if any(x == 'H' for x in self._fvalues(['SC', 'SI', 'SA']).values()):
            return 1
        return 2


class EQ5(_EQ):
    """
    EQ5 reprecentation for CVSS4

    See: see table 28 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    vector_keys = ['E']
    _maxes = {
        0: ['E:A/'],
        1: ['E:P/'],
        2: ['E:U/'],
    }
    _severity = {
        0: 1,
        1: 1,
        2: 1,
    }

    @property
    def value(self) -> int:
        value = self._values['E']
        if value == 'A':
            return 0
        if value == 'P':
            return 1
        return 2


class EQ6(_EQ):
    """
    EQ6 reprecentation for CVSS4

    See: see table 29 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    vector_keys = ['CR', 'IR', 'AR', 'VC', 'VI', 'VA']

    @property
    def value(self) -> int:
        if (all(x == 'H' for x in self._fvalues(['CR', 'VC']).values())
                or all(x == 'H' for x in self._fvalues(['IR', 'VI']).values())
                or all(x == 'H' for x in self._fvalues(['AR', 'VA']).values())):
            return 0
        return 1

    @property
    def maxes(self) -> None:
        raise TypeError('Use EQ3EQ6 for maxes')

    @property
    def max_severity(self) -> None:
        raise TypeError('Use EQ3EQ6 for max_severity')


class EQ3EQ6:
    """
    Special EQ3 and EQ6 class to handle the combination of those to.

    See: see table 30 in the CVSS 4.0 specifications
    https://www.first.org/cvss/v4.0/specification-document
    """
    _maxes = {
        0: {
            0: ['VC:H/VI:H/VA:H/CR:H/IR:H/AR:H/'],
            1: [
                'VC:H/VI:H/VA:L/CR:M/IR:M/AR:H/',
                'VC:H/VI:H/VA:H/CR:M/IR:M/AR:M/',
            ],
        },
        1: {
            0: [
                'VC:L/VI:H/VA:H/CR:H/IR:H/AR:H/',
                'VC:H/VI:L/VA:H/CR:H/IR:H/AR:H/',
            ],
            1: [
                'VC:L/VI:H/VA:L/CR:H/IR:M/AR:H/',
                'VC:L/VI:H/VA:H/CR:H/IR:M/AR:M/',
                'VC:H/VI:L/VA:H/CR:M/IR:H/AR:M/',
                'VC:H/VI:L/VA:L/CR:M/IR:H/AR:H/',
                'VC:L/VI:L/VA:H/CR:H/IR:H/AR:M/',
            ],
        },
        2: {
            1: ['VC:L/VI:L/VA:L/CR:H/IR:H/AR:H/'],
        },
    }
    _severity = {
        0: {0: 7, 1: 6},
        1: {0: 8, 1: 8},
        2: {1: 10},
    }

    def __init__(self, eq3: EQ3, eq6: EQ6) -> None:
        self._eq3 = eq3
        self._eq6 = eq6

    @property
    def maxes(self) -> list[str]:
        return self._maxes[self._eq3.value][self._eq6.value]

    @property
    def max_severity(self) -> Decimal:
        return self._severity[self._eq3.value][self._eq6.value] * Decimal('0.1')


class EQManager:
    """
    Manage the 6 EQ instances and provide access to there value

    Arguments:
      vector: CVSS4Vector vector reprecentation
    """

    def __init__(self, vector: CVSS4Vector) -> None:
        self._vector = vector
        self.eqs = [
            EQ1(vector), EQ2(vector), EQ3(vector), EQ4(vector),
            EQ5(vector), EQ6(vector),
        ]
        self._eq3eq6 = EQ3EQ6(self.eqs[2], self.eqs[5])

    @property
    def value(self) -> str:
        """ The 6 digit string reprecenting the 6 EQs """
        return ''.join(str(x) for x in self.eqs)

    @property
    def maxes(self) -> Generator[CVSS4Vector]:
        """ The max vectors of the calculated EQ values """
        for eq1 in self.eq(1).maxes:
            for eq2 in self.eq(2).maxes:
                for eq3eq6 in self.eq(3).maxes:
                    for eq4 in self.eq(4).maxes:
                        for eq5 in self.eq(5).maxes:
                            yield CVSS4Vector(f'{eq1}{eq2}{eq3eq6}{eq4}{eq5}', partial=True)

    def eq(self, eq: int, direct: bool = False) -> _EQ:
        """
        Access to the EQ of the given digit

        This is a mapper to avoid confusion about the eqs list (starting with 0)
        and the EQ number starting with 1

        Argument:
          eq: EQ number starting with 1
          direct: return the EQ3 instance instead the EQ3EQ6 instance

        Returns:
          The requested EQ instance, except for eq = 3. If direct is set to False
          (default) this will return the combination object EQ3EQ6

        Raises:
          IndexError for a invalid EQ number
        """
        if eq == 3 and not direct:
            return self._eq3eq6
        return self.eqs[eq - 1]

    def nextLower(self, eq: int) -> str:
        """
        Calculate the next lower value for the given EQ

        This calculation is based on the reference implementation.

        Argument:
          eq: EQ number starting with 1

        Returns:
          The next lower value for the given EQ
        """
        values = [x.value for x in self.eqs]
        if eq == 3:
            eq3 = values[2]
            eq6 = values[5]
            if eq3 in [0, 1] and eq6 == 1:
                values[2] += 1
                return ''.join(str(x) for x in values)
            if eq3 == 1 and eq6 == 0:
                values[5] += 1
                return ''.join(str(x) for x in values)
            if eq3 == 0 and eq6 == 0:
                l_values = list(values)
                l_values[5] += 1
                l_value = ''.join(str(x) for x in l_values)
                r_values = list(values)
                r_values[2] += 1
                r_value = ''.join(str(x) for x in r_values)
                l_score = SCORE_MAP.get(l_value)
                r_score = SCORE_MAP.get(r_value)
                if l_score and r_score and l_score > r_score:
                    return l_value
                return r_value
        values[eq - 1] += 1
        return ''.join(str(x) for x in values)

    def nextLowerScore(self, eq: int) -> Decimal | None:
        """
        Get the next lower score for the given EQ based on the calculation done in
        the nextLower method above.

        Arguments:
          eq: EQ number starting with 1

        Returns:
          The Decimal score from the calculated next lower value or None if no score
          mapping is found.
        """
        return SCORE_MAP.get(self.nextLower(eq))

    def maxSeverity(self, eq: int) -> Decimal:
        """
        Get the max severity for the given EQ number

        Arguments:
          eq: EQ number starting with 1

        Returns:
          Decimal max severity of the EQ value
        """
        return self.eq(eq).max_severity
