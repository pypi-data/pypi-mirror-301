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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Neo4jClient:
    URI = os.environ["NEO4J_URI"]
    DATABASE = os.environ["NEO4J_DATABASE"]
    AUTH = (os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])

    NODE_LABEL_PROP_KEY = "name"

    def __init__(self):
        self.driver = GraphDatabase.driver(Neo4jClient.URI, auth=Neo4jClient.AUTH)
        self.database = Neo4jClient.DATABASE

    def close(self):
        self.driver.close()

    def __node_with_prop_exists(self, node_type: str, prop_key: str, prop_value: str):
        records = self.driver.execute_query(
            f"MATCH (node:{node_type}) WHERE node.{prop_key} = $value RETURN node",
            value=prop_value,
            database_=Neo4jClient.DATABASE,
        ).records

        return len(records) > 0

    def save_a_node_with_attributes(self, node_type: str, attributes: dict):
        if self.__node_with_prop_exists(
                node_type,
                Neo4jClient.NODE_LABEL_PROP_KEY,
                attributes[Neo4jClient.NODE_LABEL_PROP_KEY]
        ):
            logging.info(f"node: {attributes} already exists in database")
            return

        logging.info(f"Creating node {attributes}...")
        return self.driver.execute_query(
            f"CREATE (node:{node_type} $attributes) RETURN node",
            attributes=attributes,
            database_=Neo4jClient.DATABASE,
        ).summary

    def save_a_link_with_attributes(self, language: str, source_label: str, target_label: str, attributes: dict):
        if self.__node_with_prop_exists("Term", Neo4jClient.NODE_LABEL_PROP_KEY, target_label):
            self.driver.execute_query(
                f"""
                MATCH
                    (term:Term WHERE term.{Neo4jClient.NODE_LABEL_PROP_KEY} = $term AND term.language = $language),
                    (related:Term WHERE related.{Neo4jClient.NODE_LABEL_PROP_KEY} = $related_term AND
                    term.language = $language)
                CREATE
                    (term)-[:RELATED $attributes]->(related)
                """,
                language=language,
                term=source_label,
                related_term=target_label,
                attributes=attributes
            )
        else:
            self.driver.execute_query(
                f"""
                MATCH
                    (term:Term WHERE term.{Neo4jClient.NODE_LABEL_PROP_KEY} = $term AND term.language = $language),
                    (definition:Definition WHERE definition.{Neo4jClient.NODE_LABEL_PROP_KEY} = $definition)
                CREATE
                    (term)-[:DEFINITION $attributes]->(definition)
                """,
                language=language,
                term=source_label,
                definition=target_label,
                attributes=attributes
            )


def get_database_client():
    return Neo4jClient()


def get_node_label_attribute_key() -> str:
    return Neo4jClient.NODE_LABEL_PROP_KEY
