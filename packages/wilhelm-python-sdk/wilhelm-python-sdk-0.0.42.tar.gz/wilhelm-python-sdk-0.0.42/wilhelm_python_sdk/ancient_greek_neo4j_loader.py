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
import logging
import os

from neo4j import GraphDatabase

from wilhelm_python_sdk.vocabulary_database_loader import ANCIENT_GREEK
from wilhelm_python_sdk.vocabulary_database_loader import get_definitions
from wilhelm_python_sdk.vocabulary_database_loader import get_vocabulary
from wilhelm_python_sdk.vocabulary_database_loader import \
    save_a_link_with_attributes
from wilhelm_python_sdk.vocabulary_database_loader import \
    save_a_node_with_attributes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URI = os.environ["NEO4J_URI"]
DATABASE = os.environ["NEO4J_DATABASE"]
AUTH = (os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])


def get_attributes(word: object) -> dict:
    attributes = {"name": word["term"], "language": ANCIENT_GREEK}

    return attributes


def load_into_database(yaml_path: str):
    """
    Upload https://github.com/QubitPi/wilhelm-vocabulary/blob/master/ancient-greek.yaml to Neo4j Database.

    :param yaml_path:  The absolute or relative path (to the invoking script) to the YAML file above
    """
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

    vocabulary = get_vocabulary(yaml_path)

    for word in vocabulary:
        term = word["term"]

        save_a_node_with_attributes(driver, "Term", get_attributes(word))

        definitions = get_definitions(word)
        for definition_with_predicate in definitions:
            predicate = definition_with_predicate[0]
            definition = definition_with_predicate[1]

            save_a_node_with_attributes(driver, "Definition", {"name": definition})

            if predicate:
                save_a_link_with_attributes(ANCIENT_GREEK, driver, term, definition, {"name": predicate})
            else:
                save_a_link_with_attributes(ANCIENT_GREEK, driver, term, definition, {"name": "definition"})
