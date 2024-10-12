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
import re

import yaml
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE = os.environ["NEO4J_DATABASE"]

GERMAN = "German"
LATIN = "Latin"
ANCIENT_GREEK = "Ancient Greek"

DRIVER = None
with GraphDatabase.driver(
        os.environ["NEO4J_URI"], auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
) as driver:
    DRIVER = driver


def get_vocabulary(yaml_path: str) -> list:
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)["vocabulary"]


def get_definitions(word) -> list[(str, str)]:
    """
    Extract definitions from a word as a list of bi-tuples, with the first element being the predicate and the second
    being the definition.

    For example::

    definition:
      - term: nämlich
        definition:
          - (adj.) same
          - (adv.) namely
          - because

    The method will return `[("adj.", "same"), ("adv.", "namely"), (None, "because")]`

    The method works for the single-definition case, i.e.::

    definition:
      - term: na klar
        definition:

    returns a list of one tupple `[(None, "of course")]`

    Note that any definition are converted to string. If the word does not contain a field named exactly "definition", a
    ValueError is raised.

    :param word:  A dictionary that contains a "definition" key whose value is either a single-value or a list of
                  single-values
    :return: a list of two-element tuples, where the first element being the predicate (can be `None`) and the second
             being the definition
    """
    logging.info("Extracting definitions from {}".format(word))

    if "definition" not in word:
        raise ValueError("{} does not contain 'definition' field. Maybe there is a typo".format(word))

    predicate_with_definition = []

    definitions = [word["definition"]] if not isinstance(word["definition"], list) else word["definition"]

    for definition in definitions:
        definition = str(definition)

        definition = definition.strip()

        match = re.match(r"\((.*?)\)", definition)
        if match:
            predicate_with_definition.append((match.group(1), re.sub(r'\(.*?\)', '', definition).strip()))
        else:
            predicate_with_definition.append((None, definition))

    return predicate_with_definition


def node_with_label_exists(label: str, node_type: str):
    records = DRIVER.execute_query(
        f"MATCH (node:{node_type}) WHERE node.name = $name RETURN node",
        name=label,
        database_=DATABASE,
    ).records

    return len(records) > 0


def save_a_node_with_attributes(node_type: str, attributes: dict):
    if node_with_label_exists(attributes["name"], node_type):
        logging.info(f"node: {attributes} already exists in database")
        return

    logging.info(f"Creating node {attributes}...")
    return DRIVER.execute_query(
        f"CREATE (node:{node_type} $attributes) RETURN node",
        attributes=attributes,
        database_=DATABASE,
    ).summary


def save_a_link_with_attributes(language: str, source_name: str, target_name: str, attributes: dict):
    if node_with_label_exists(target_name, "Term"):
        DRIVER.execute_query(
            """
            MATCH
                (term:Term WHERE term.name = $term AND term.language = $language),
                (related:Term WHERE related.name = $related_term AND term.language = $language)
            CREATE
                (term)-[:RELATED $attributes]->(related)
            """,
            term=source_name,
            language=language,
            related_term=target_name,
            attributes=attributes
        )
    else:
        DRIVER.execute_query(
            """
            MATCH
                (term:Term WHERE term.name = $term AND term.language = $language),
                (definition:Definition WHERE definition.name = $definition)
            CREATE
                (term)-[:DEFINITION $attributes]->(definition)
            """,
            term=source_name,
            language=language,
            definition=target_name,
            attributes=attributes
        )
