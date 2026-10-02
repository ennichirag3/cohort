import json
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load connection details from prototype/backend/.env
load_dotenv(Path(__file__).with_name(".env"))

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

if not all([uri, username, password]):
    raise RuntimeError(
        "Set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD "
        "in prototype/backend/.env"
    )

data_path = Path(__file__).parent / "data" / "pallets_click_sample.json"
with data_path.open(encoding="utf-8") as file:
    data = json.load(file)

driver = GraphDatabase.driver(uri, auth=(username, password))


def import_data(tx, data):
    repo = data["repository"]

    tx.run(
        """
        MERGE (r:Repository {id: $id})
        SET r.name = $name,
            r.source_url = $source_url,
            r.url = $source_url
        """,
        id=repo["id"],
        name=repo["name"],
        source_url=repo["source_url"],
    )

    for commit in data["commits"]:
        tx.run(
            """
            MATCH (r:Repository {id: $repo_id})
            MERGE (c:Commit {id: $commit_id})
            SET c.message = $message,
                c.date = $date,
                c.author = $author,
                c.source_url = $source_url,
                c.url = $source_url
            MERGE (r)-[:HAS_COMMIT]->(c)
            """,
            repo_id=repo["id"],
            commit_id=commit["id"],
            message=commit.get("message", ""),
            date=commit.get("committed_at"),
            author=commit.get("author_login"),
            source_url=commit.get("source_url"),
        )

        author = commit.get("author_login")
        if author:
            tx.run(
                """
                MATCH (c:Commit {id: $commit_id})
                MERGE (d:Developer {id: $developer_id})
                SET d.login = $login
                MERGE (c)-[:AUTHORED_BY]->(d)
                """,
                commit_id=commit["id"],
                developer_id=f"github:{author}",
                login=author,
            )

        for path in commit.get("files", []):
            tx.run(
                """
                MATCH (c:Commit {id: $commit_id})
                MERGE (f:File {id: $file_id})
                SET f.path = $path
                MERGE (c)-[:CHANGED]->(f)
                """,
                commit_id=commit["id"],
                file_id=f'{repo["id"]}:{path}',
                path=path,
            )

    for issue in data.get("issues", []):
        tx.run(
            """
            MERGE (i:Issue {id: $id})
            SET i.title = $title,
                i.body = $body,
                i.author = $author,
                i.created_at = $created_at,
                i.source_url = $source_url,
                i.url = $source_url
            """,
            id=issue["id"],
            title=issue.get("title", ""),
            body=issue.get("body_excerpt", ""),
            author=issue.get("author_login"),
            created_at=issue.get("created_at"),
            source_url=issue.get("source_url"),
        )

    for pull_request in data.get("pull_requests", []):
        tx.run(
            """
            MATCH (r:Repository {id: $repo_id})
            MERGE (p:PullRequest {id: $id})
            SET p.title = $title,
                p.body = $body,
                p.author = $author,
                p.source_url = $source_url,
                p.url = $source_url,
                p.created_at = $created_at,
                p.merged_at = $merged_at
            """,
            repo_id=repo["id"],
            id=pull_request["id"],
            title=pull_request.get("title", ""),
            body=pull_request.get("body", ""),
            author=pull_request.get("author_login"),
            source_url=pull_request.get("source_url"),
            created_at=pull_request.get("created_at"),
            merged_at=pull_request.get("merged_at"),
        )

        for commit_id in pull_request.get("commit_ids", []):
            tx.run(
                """
                MATCH (p:PullRequest {id: $pr_id})
                MATCH (c:Commit {id: $commit_id})
                MERGE (p)-[:INCLUDES_COMMIT]->(c)
                """,
                pr_id=pull_request["id"],
                commit_id=commit_id,
            )

        for issue_id in pull_request.get("issue_ids", []):
            tx.run(
                """
                MATCH (p:PullRequest {id: $pr_id})
                MATCH (i:Issue {id: $issue_id})
                MERGE (p)-[:REFERENCES_ISSUE]->(i)
                """,
                pr_id=pull_request["id"],
                issue_id=issue_id,
            )


try:
    with driver.session() as session:
        session.execute_write(import_data, data)
    print("Sample data imported into Neo4j.")
finally:
    driver.close()