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
from wilhelm_python_sdk.database_clients import get_database_client
from wilhelm_python_sdk.database_clients import get_node_label_attribute_key
from wilhelm_python_sdk.vocabulary_parser import GERMAN
from wilhelm_python_sdk.vocabulary_parser import get_attributes
from wilhelm_python_sdk.vocabulary_parser import get_definitions
from wilhelm_python_sdk.vocabulary_parser import get_vocabulary

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


def load_into_database(yaml_path: str):
    """
    Upload https://github.com/QubitPi/wilhelm-vocabulary/blob/master/german.yaml to Neo4j Database.

    :param yaml_path:  The absolute or relative path (to the invoking script) to the YAML file above
    """
    vocabulary = get_vocabulary(yaml_path)
    link_hints = {}
    database_client = get_database_client()
    label_key = get_node_label_attribute_key()

    for word in vocabulary:
        attributes = get_attributes(word, GERMAN, label_key)

        link_hints = update_link_hints(link_hints, attributes, word["term"])

        database_client.save_a_node_with_attributes("Term", attributes)
        definitions = get_definitions(word)
        for definition_with_predicate in definitions:
            definition = definition_with_predicate[1]
            database_client.save_a_node_with_attributes("Definition", {label_key: definition})

    # save links between term and definitions
    for word in vocabulary:
        definitions = get_definitions(word)
        for definition_with_predicate in definitions:
            predicate = definition_with_predicate[0]
            definition = definition_with_predicate[1]
            term = word["term"]
            if predicate:
                database_client.save_a_link_with_attributes(
                    language=GERMAN,
                    source_label=term,
                    target_label=definition,
                    attributes={label_key: predicate}
                )
            else:
                database_client.save_a_link_with_attributes(
                    language=GERMAN,
                    source_label=term,
                    target_label=definition,
                    attributes={label_key: "definition"}
                )

    # save link_hints as database links
    for word in vocabulary:
        term = word["term"]
        attributes = get_attributes(word, GERMAN, label_key)

        for attribute_value in attributes.values():
            if (attribute_value in link_hints) and (term != link_hints[attribute_value]):
                database_client.save_a_link_with_attributes(
                    language=GERMAN,
                    source_label=term,
                    target_label=link_hints[attribute_value],
                    attributes={label_key: f"sharing declensions: {link_hints[attribute_value]}"}
                )
