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

from wilhelm_python_sdk.vocabulary_database_loader import GERMAN
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

EXCLUDED_DECLENSION_ENTRIES = [
    "",
    "singular",
    "plural",
    "masculine",
    "feminine",
    "neuter",
    "nominative",
    "genitive",
    "dative",
    "accusative",
    "N/A"
]


def get_declension_attributes(word: object) -> dict[str, str]:
    """
    Returns noun-specific attributes as a flat map.

    If the noun's declension is, for some reasons, "Unknown", this function will return an empty dict. Otherwise, the
    declension table is flattened like with row-col index in the map key::

    "declension-0-0": "",
    "declension-0-1": "singular",
    "declension-0-2": "singular",
    "declension-0-3": "singular",
    "declension-0-4": "plural",
    "declension-0-5": "plural",

    :param word:  A vocabulary representing a German noun

    :return: a flat map containing all the YAML encoded information about the noun excluding term and definition
    """

    declension = word["declension"]

    if declension == "Unknown":
        return {}

    attributes = {}
    for i, row in enumerate(declension):
        for j, col in enumerate(row):
            attributes[f"declension-{i}-{j}"] = declension[i][j]

    return attributes


def get_attributes(word: object) -> dict[str, str]:
    """
    Returns a flat map as the Term node properties stored in Neo4J.

    :param word:  A German vocabulary representing

    :return: a flat map containing all the YAML encoded information about the vocabulary
    """
    attributes = {"name": word["term"], "language": GERMAN}

    if "declension" in word:
        attributes = attributes | get_declension_attributes(word)

    return attributes


def update_link_hints(link_hints: dict[str, str], attributes: dict[str, str], term: str):
    """
    Update and prepare a mapping between shared attribute values (key) to the term that has that attribute (value).

    This mapping will be used to create more links in graph database.

    The operation calling this method was inspired by the spotting the relationship between "die Reise" and "der Reis"
    who share large portions of their declension table. In this case, there will be a link between "die Reise" and
    "der Reis". Linking the vocabulary this way helps memorize vocabulary more efficiently

    :param link_hints:  The mapping
    :param attributes:  The source of mapping hints
    :param term:  the term that has the attribute
    """
    for key, value in attributes.items():
        if key.startswith("declension-") and value not in EXCLUDED_DECLENSION_ENTRIES:
            link_hints[value] = term
    return link_hints


def save_relationships_between_term_and_definitions(vocabulary, driver):
    for word in vocabulary:
        definitions = get_definitions(word)
        for definition_with_predicate in definitions:
            predicate = definition_with_predicate[0]
            definition = definition_with_predicate[1]
            term = word["term"]
            if predicate:
                save_a_link_with_attributes(
                    language=GERMAN,
                    database_driver=driver,
                    source_name=term,
                    target_name=definition,
                    attributes={"name": predicate}
                )
            else:
                save_a_link_with_attributes(
                    language=GERMAN,
                    database_driver=driver,
                    source_name=term,
                    target_name=definition,
                    attributes={"name": "definition"}
                )


def save_link_hints_relationships(link_hints, vocabulary, driver):
    for word in vocabulary:
        term = word["term"]
        attributes = get_attributes(word)

        for attribute_value in attributes.values():
            if (attribute_value in link_hints) and (term != link_hints[attribute_value]):
                save_a_link_with_attributes(
                    language=GERMAN,
                    database_driver=driver,
                    source_name=term,
                    target_name=link_hints[attribute_value],
                    attributes={"name": f"sharing declensions: {link_hints[attribute_value]}"}
                )


def load_into_database(yaml_path: str):
    """
    Upload https://github.com/QubitPi/wilhelm-vocabulary/blob/master/german.yaml to Neo4j Database.

    :param yaml_path:  The absolute or relative path (to the invoking script) to the YAML file above
    """
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

    vocabulary = get_vocabulary(yaml_path)
    link_hints = {}

    for word in vocabulary:
        attributes = get_attributes(word)

        link_hints = update_link_hints(link_hints, attributes, word["term"])

        save_a_node_with_attributes(driver, "Term", attributes)
        definitions = get_definitions(word)
        for definition_with_predicate in definitions:
            definition = definition_with_predicate[1]
            save_a_node_with_attributes(driver, "Definition", {"name": definition})

    save_relationships_between_term_and_definitions(vocabulary, driver)
    save_link_hints_relationships(link_hints, vocabulary, driver)
