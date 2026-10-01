MATCH (r:Repository {id: "demo-repository"})-[:HAS_COMMIT]->(c:Commit)
OPTIONAL MATCH (c)-[:CHANGED]->(f:File)
OPTIONAL MATCH (pr:PullRequest)-[:INCLUDES_COMMIT]->(c)
RETURN
    r.name AS repository,
    c.id AS commit_id,
    c.message AS commit_message,
    c.date AS committed_at,
    f.path AS changed_file,
    pr.id AS pull_request_id,
    pr.title AS pull_request_title,
    coalesce(pr.url, pr.source_url) AS pull_request_url,
    coalesce(c.url, c.source_url) AS commit_url
ORDER BY committed_at;

