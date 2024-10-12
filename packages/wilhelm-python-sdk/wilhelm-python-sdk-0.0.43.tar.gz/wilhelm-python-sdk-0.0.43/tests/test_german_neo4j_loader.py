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

from wilhelm_python_sdk.german_loader import EXCLUDED_DECLENSION_ENTRIES
from wilhelm_python_sdk.german_loader import update_link_hints


class TestGermanNeo4JLoader(unittest.TestCase):

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
