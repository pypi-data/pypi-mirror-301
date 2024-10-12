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

from wilhelm_python_sdk.vocabulary_database_loader import get_definitions


class TestLoader(unittest.TestCase):

    def test_get_definitions(self):
        self.assertEqual(
            [("adj.", "same"), ("adv.", "namely"), (None, "because")],
            get_definitions({
                "definition": ["(adj.) same", "(adv.) namely", "because"]
            }),
        )

    def test_single_definition_term(self):
        self.assertEqual(
            [(None, "one")],
            get_definitions({
                "definition": "one"
            }),
        )

    def test_numerical_definition(self):
        self.assertEqual(
            [(None, "1")],
            get_definitions({
                "definition": 1
            }),
        )

    def test_missing_definition(self):
        with self.assertRaises(ValueError):
            get_definitions({"defintion": "I'm 23 years old."})
