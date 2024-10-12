# Copyright Jiaqi (Hutao of Emberfire)
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
import unittest

import yaml

from wilhelm_python_sdk.german_neo4j_loader import EXCLUDED_DECLENSION_ENTRIES
from wilhelm_python_sdk.german_neo4j_loader import get_attributes
from wilhelm_python_sdk.german_neo4j_loader import update_link_hints

UNKOWN_DECLENSION_NOUN_YAML = """
    term: die Grilltomate
    definition: the grilled tomato
    declension: Unknown
"""

HUT_YAML = """
    term: der Hut
    definition: the hat
    declension:
      - ["",         singular,      plural]
      - [nominative, Hut,           Hüte  ]
      - [genitive,   "Hutes, Huts", Hüte  ]
      - [dative,     Hut,           Hüten ]
      - [accusative, Hut,           Hüte  ]
"""

HUT_DECLENSION_MAP = {
    "declension-0-0": "",
    "declension-0-1": "singular",
    "declension-0-2": "plural",

    "declension-1-0": "nominative",
    "declension-1-1": "Hut",
    "declension-1-2": "Hüte",

    "declension-2-0": "genitive",
    "declension-2-1": "Hutes, Huts",
    "declension-2-2": "Hüte",

    "declension-3-0": "dative",
    "declension-3-1": "Hut",
    "declension-3-2": "Hüten",

    "declension-4-0": "accusative",
    "declension-4-1": "Hut",
    "declension-4-2": "Hüte",
}


class TestGermanNeo4JLoader(unittest.TestCase):

    def test_get_attributes(self):
        self.assertEqual(
            {"name": "der Hut", "language": "German"} | HUT_DECLENSION_MAP,
            get_attributes(yaml.safe_load(HUT_YAML)),
        )

    def test_update_link_hints(self):
        self.assertEqual(
            {"Reis": "der Reis", "Reise": "der Reis"},
            update_link_hints({}, {"declension-1-1": "Reis", "declension-1-2": "Reise"}, "der Reis")
        )

    def test_all_declension_tables_values_that_are_not_used_for_link_reference(self):
        all_cases_declension_map = dict([(f"declension-{value}", value) for value in EXCLUDED_DECLENSION_ENTRIES])
        actual = update_link_hints({}, all_cases_declension_map, "der Hut")
        for value in all_cases_declension_map.values():
            self.assertTrue(value not in actual)
