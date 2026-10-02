import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

OWNER = "pallets"
REPO = "click"
LIMIT = 3

API = f"https://api.github.com/repos/{OWNER}/{REPO}"
repo_id = f"{OWNER}/{REPO}"


def get_json(path):
    request = Request(
        f"https://api.github.com/repos/{OWNER}/{REPO}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "hackfront-cohort-sample-ingestion",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def author_login(record):
    user = record.get("user") or record.get("author") or {}
    return user.get("login")


def make_issue(issue):
    number = issue["number"]
    return {
        "id": f"{repo_id}#{number}",
        "number": number,
        "title": issue.get("title") or "",
        "author_login": author_login(issue),
        "created_at": issue.get("created_at"),
        "source_url": issue.get("html_url"),
        "body_excerpt": (issue.get("body") or "")[:3000],
    }


repository_info = get_json("")

data = {
    "repository": {
        "id": repo_id,
        "name": repository_info["name"],
        "source_url": repository_info["html_url"],
    },
    "commits": [],
    "pull_requests": [],
    "issues": [],
}

commits_by_sha = {}
issues_by_id = {}


def add_commit(sha, pull_request_id=None):
    if sha not in commits_by_sha:
        commit = get_json(f"/commits/{sha}")
        author = commit.get("author") or {}
        commit_details = commit.get("commit") or {}
        author_details = commit_details.get("author") or {}

        commits_by_sha[sha] = {
            "id": f"{repo_id}@{sha}",
            "sha": sha,
            "message": commit_details.get("message") or "",
            "author_login": author.get("login"),
            "committed_at": author_details.get("date"),
            "source_url": commit.get("html_url"),
            "files": [
                changed_file["filename"]
                for changed_file in commit.get("files", [])
            ],
            "pull_request_ids": [],
        }

    if pull_request_id:
        linked_prs = commits_by_sha[sha]["pull_request_ids"]
        if pull_request_id not in linked_prs:
            linked_prs.append(pull_request_id)


def add_issue(number):
    issue_id = f"{repo_id}#{number}"
    if issue_id in issues_by_id:
        return issue_id

    issue = get_json(f"/issues/{number}")

    # GitHub's issues endpoint also returns pull requests.
    if issue.get("pull_request"):
        return None

    issues_by_id[issue_id] = make_issue(issue)
    return issue_id


# Fetch a small recent sample of commits, with changed file paths.
for item in get_json(f"/commits?per_page={LIMIT}"):
    add_commit(item["sha"])

# Fetch a small sample of closed PRs and the commits they contain.
pull_requests = get_json(
    f"/pulls?state=closed&sort=updated&direction=desc&per_page={LIMIT}"
)

for pr in pull_requests:
    pr_id = f"{repo_id}#{pr['number']}"
    pr_body = pr.get("body") or ""

    commit_summaries = get_json(
        f"/pulls/{pr['number']}/commits?per_page=100"
    )
    commit_ids = []

    for item in commit_summaries:
        sha = item["sha"]
        add_commit(sha, pr_id)
        commit_ids.append(f"{repo_id}@{sha}")

    # Only create issue links for explicit GitHub closing phrases,
    # such as "Fixes #123". A mere mention is not treated as a link.
    issue_numbers = re.findall(
        r"(?i)\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+#(\d+)\b",
        pr_body,
    )
    issue_ids = []

    for number_text in issue_numbers:
        issue_id = add_issue(int(number_text))
        if issue_id and issue_id not in issue_ids:
            issue_ids.append(issue_id)

    data["pull_requests"].append({
        "id": pr_id,
        "number": pr["number"],
        "title": pr.get("title") or "",
        "body": pr_body,
        "author_login": author_login(pr),
        "created_at": pr.get("created_at"),
        "merged_at": pr.get("merged_at"),
        "source_url": pr.get("html_url"),
        "commit_ids": commit_ids,
        "issue_ids": issue_ids,
    })

# Fetch a few regular issues. Pull requests are filtered out.
issue_summaries = get_json(
    f"/issues?state=all&sort=updated&direction=desc&per_page={LIMIT * 3}"
)

for issue in issue_summaries:
    if not issue.get("pull_request"):
        item = make_issue(issue)
        issues_by_id[item["id"]] = item

data["commits"] = list(commits_by_sha.values())
data["issues"] = list(issues_by_id.values())

output_path = Path(__file__).parent / "data" / "pallets_click_sample.json"
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as output_file:
    json.dump(data, output_file, indent=2, ensure_ascii=False)

print(f"Saved normalized sample to: {output_path}")
print(
    f"Repositories: 1 | Commits: {len(data['commits'])} | "
    f"Pull requests: {len(data['pull_requests'])} | "
    f"Issues: {len(data['issues'])}"
)