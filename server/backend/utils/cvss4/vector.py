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


class CVSS4Vector:
    """
    CVSS 4.0 vector representation

    This instance provides easy access to the different keys of a vector string.

    Arguments:
      vector: CVSS 4.0 vector as string
      partial: If set, allow only parts of a vector string
    """
    keys = [
        'AV', 'PR', 'UI',
        'AC', 'AT',
        'VC', 'VI', 'VA',
        'SC', 'SI', 'SA',
        'MSI', 'MSA',
        'CR', 'IR', 'AR',
        'E',
    ]

    @classmethod
    def load(cls, data: dict[str, str]) -> CVSS4Vector:
        """
        Load the vector from a dict instance

        Arguments:
          data: vector reprecented as dict

        Returns:
          CVSS4Vector instance
        """
        sections = ['CVSS:4.0']
        for (name, value) in data.items():
            sections.append(f'{name.upper()}:{value}')
        return cls('/'.join(sections))

    def __init__(self, vector: str, partial: bool = False) -> None:
        self.vector = vector.strip('/')
        self._data = {x: None for x in self.keys}
        parts = self.vector.split('/')
        if not partial:
            parts.pop(0)
        for part in parts:
            (name, value) = part.split(':')
            self._data[name] = value

    def __str__(self) -> str:
        return self.vector

    def __getattr__(self, key: str) -> str:
        try:
            return self._data[key]
        except KeyError as exc:
            raise AttributeError() from exc

    def get(self, key: str) -> str | None:
        """
        Get the value of a given vector key.

        As described in the specification there are some special cases:
          - no 'E' value is set: return 'A' as value
          - no 'CR', 'IR' or 'AR' value is set: return 'H' as value
          - modifier values (see below)

        If there are modifier values set for requested keys, the modifier value is
        returned. E.g. if the modifier MSI is set, and the key SI is requested, the
        value of MSI is returned instead of the SI value.

        Arguments:
          key: vector key to get

        Returns:
          The value of the given vector key, with the modifications desribed above,
          or None if not found.
        """
        value = self._data.get(key)
        if not value or value == 'X':
            if key == 'E':
                return 'A'
            if key in ['CR', 'IR', 'AR']:
                return 'H'
        modified = self._data.get(f'M{key}')
        if modified:
            return modified
        return value

    def asdict(
            self, kfilter: list[str] | None = None, lower: bool = False,
    ) -> dict:
        """
        Get the vector string as dict

        The dict will be build based on the defaults and exceptions described in the
        get method above.
        In addition the method supports a filter for keys.

        Arguments:
          kfilter: list of vector keys which should only be included in the dict
          lower: return the vector keys as lower letters

        Returns:
          dict based on the filter
        """
        data = {x: self.get(x) for x in self.keys}
        if kfilter:
            data = {x[0]: x[1] for x in filter(lambda x: x[0] in kfilter, data.items())}
        if lower is True:
            return {k.lower(): v for k, v in data.items()}
        return dict(data)
