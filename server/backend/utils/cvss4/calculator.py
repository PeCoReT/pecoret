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

import logging
from decimal import Decimal

from .eq import EQManager
from .maps import SCORE_MAP, LEVELS
from .vector import CVSS4Vector

log = logging.getLogger(__name__)


class CVSS4Calculator:
    """
    CVSS4Calculator

    class instance to calculate the CVSS 4.0 score based on a given vector string.

    Usage:
      from cvss4 import CVSS4Calculator
      score =
      CVSS4Calculator.calc('CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:A/MSI:S')
    """

    @classmethod
    def calc(cls, vector: CVSS4Vector | str) -> Decimal:
        """
        Calculate the score of the given vector

        Arguments:
          vector: CVSS4Vector to get the score from

        Returns:
          The CVSS score as Decimal
        """
        if isinstance(vector, str):
            vector = CVSS4Vector(vector)
        none_check = ['VC', 'VI', 'VA', 'SC', 'SI', 'SA']
        if all(x == 'N' for x in vector.asdict(none_check).values()):
            log.debug('[cvss4] V* and S* is None, score 0.0')
            return Decimal('0.0')
        eqmanager = EQManager(vector)
        value = SCORE_MAP[eqmanager.value]
        log.debug('[cvss4] base score: %f', value)
        for max_vector in eqmanager.maxes:
            severity = {}
            for key in CVSS4Vector.keys:
                if key in ['MSI', 'MSA']:
                    continue
                vector_value = vector.get(key)
                max_value = max_vector.get(key)
                if not max_value:
                    severity[key] = LEVELS[key][vector_value]
                else:
                    severity[key] = LEVELS[key][vector_value] - LEVELS[key][max_value]
            if any(x < 0 for x in severity.values()):
                continue
            break
        current_severities = [
            sum(x[1] for x in severity.items() if x[0] in ['AV', 'PR', 'UI']),
            sum(x[1] for x in severity.items() if x[0] in ['AC', 'AT']),
            sum(x[1] for x in severity.items() if x[0] in ['VC', 'VI', 'VA', 'CR', 'IR', 'AR']),  # noqa: E501
            sum(x[1] for x in severity.items() if x[0] in ['SC', 'SI', 'SA']),
            0,  # eq5
        ]
        if logging.root.level == logging.DEBUG:
            # only run when in debug logging
            for i, v in enumerate(current_severities):
                log.debug('[cvss4] (eq%d) calculated severity: %f', i + 1, v)
        available_distances = []
        for eq in range(1, 6):
            lower_score = eqmanager.nextLowerScore(eq)
            if not lower_score:
                available_distances.append(None)
            else:
                available_distances.append(value - lower_score)

        existing_lower = 0

        normalized = [0] * 5

        for i, distance in enumerate(available_distances):
            if distance:
                existing_lower += 1
                percent = current_severities[i] / eqmanager.maxSeverity(i + 1)
                normalized[i] = distance * percent
                log.debug('[cvss4] (eq%d) calculate distance: %f', i + 1, normalized[i])

        log.debug('[cvss4] existing lower scores found: %d', existing_lower)
        if existing_lower == 0:
            mean_distance = 0
        else:
            mean_distance = sum(normalized) / existing_lower

        log.debug('[cvss4] calculated mean distance: %f', mean_distance)
        value -= mean_distance
        log.debug('[cvss4] calculated value: %f', value)
        if value < 0:
            return Decimal('0.0')
        if value > 10:
            return Decimal('10.0')
        return value.quantize(Decimal('1.0'))

    @classmethod
    def from_string(cls, data):
        calc = cls().calc(data)
        score = float(calc)
        severity = cls().severity_from_score(score)
        return score, severity

    @classmethod
    def severity_from_score(cls, score):
        if score == 0.0:
            return "Informational"
        elif score <= 3.9:
            return "Low"
        elif score <= 6.9:
            return "Medium"
        elif score <= 8.9:
            return "High"
        return "Critical"
