"""Fetch a bounded, useful GitHub history dataset for the Neo4j MVP.

The defaults collect recent commits, merged pull requests, and issues. The
script also includes commits belonging to the selected pull requests so the
Neo4j importer can build PR-to-commit relationships. It does not clone the
entire repository or attempt an unbounded history download.
"""

import argparse
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
API_VERSION = "2026-03-10"
DEFAULT_OWNER = "pallets"
DEFAULT_REPO = "click"
BODY_LIMIT = 5000
MAX_PAGE_SIZE = 100


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch normalized commits, merged PRs, and issues from GitHub."
    )
    parser.add_argument("--owner", default=DEFAULT_OWNER, help="GitHub owner (default: pallets)")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="GitHub repository (default: click)")
    parser.add_argument("--commits", type=int, default=30, help="Recent commits to fetch (default: 30)")
    parser.add_argument("--pull-requests", type=int, default=20, help="Merged pull requests to fetch (default: 20)")
    parser.add_argument("--issues", type=int, default=30, help="Issues to fetch (default: 30)")
    parser.add_argument(
        "--commit-details",
        type=int,
        default=15,
        help="How many recent commits to fetch detailed changed-file lists for (default: 15)",
    )
    parser.add_argument(
        "--linked-issue-details",
        type=int,
        default=10,
        help="Maximum extra API calls to fetch issues linked by PR closing text (default: 10)",
    )
    parser.add_argument(
        "--output",
        help="Output JSON path (default: data/<owner>_<repo>_final.json)",
    )
    args = parser.parse_args()

    for name in ("commits", "pull_requests", "issues", "commit_details", "linked_issue_details"):
        value = getattr(args, name)
        if value < 0 or value > MAX_PAGE_SIZE:
            parser.error(f"--{name.replace('_', '-')} must be between 0 and {MAX_PAGE_SIZE}")

    if not args.owner.strip() or not args.repo.strip():
        parser.error("--owner and --repo cannot be empty")

    return args


class GitHubClient:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.base_url = f"{API_ROOT}/repos/{owner}/{repo}"
        self.request_count = 0
        self.token = os.getenv("GITHUB_TOKEN")

    def get_json(self, path, params=None):
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "codeinsight-public-repository-ingestion",
            "X-GitHub-Api-Version": API_VERSION,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = Request(url, headers=headers)
        self.request_count += 1
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code in (403, 429):
                raise RuntimeError(
                    "GitHub API rate limit reached. Wait and run the command again. "
                    "For a public repository, no token is required; an optional "
                    "GITHUB_TOKEN environment variable raises the API limit."
                ) from error
            if error.code == 404:
                raise RuntimeError(
                    f"GitHub could not find {self.owner}/{self.repo}{path}. "
                    "Check the owner and repository spelling."
                ) from error
            raise RuntimeError(f"GitHub API returned HTTP {error.code} for {path}.") from error
        except URLError as error:
            raise RuntimeError(f"Could not connect to GitHub: {error.reason}") from error


def author_login(record):
    user = record.get("user") or record.get("author") or {}
    return user.get("login")


def make_issue(issue, repository_id):
    return {
        "id": f"{repository_id}#{issue['number']}",
        "number": issue["number"],
        "title": issue.get("title") or "",
        "body": (issue.get("body") or "")[:BODY_LIMIT],
        "author_login": author_login(issue),
        "created_at": issue.get("created_at"),
        "updated_at": issue.get("updated_at"),
        "url": issue.get("html_url"),
        "source_url": issue.get("html_url"),
    }


def commit_record(item, repository_id):
    commit_details = item.get("commit") or {}
    author_details = commit_details.get("author") or {}
    return {
        "id": f"{repository_id}@{item['sha']}",
        "sha": item["sha"],
        "message": commit_details.get("message") or "",
        "author_login": author_login(item),
        "committed_at": author_details.get("date"),
        "url": item.get("html_url"),
        "source_url": item.get("html_url"),
        "files": [],
        "pull_request_ids": [],
    }


def add_commit(item, repository_id, commits_by_sha, pull_request_id=None):
    sha = item["sha"]
    if sha not in commits_by_sha:
        commits_by_sha[sha] = commit_record(item, repository_id)

    commit = commits_by_sha[sha]
    if pull_request_id and pull_request_id not in commit["pull_request_ids"]:
        commit["pull_request_ids"].append(pull_request_id)
    return commit


def fetch_matching(client, path, params, desired_count, predicate):
    """Read pages until enough matching records are collected or results end."""
    matches = []
    page = 1
    per_page = MAX_PAGE_SIZE

    while len(matches) < desired_count:
        page_params = {**params, "per_page": per_page, "page": page}
        batch = client.get_json(path, page_params)
        if not batch:
            break

        matches.extend(item for item in batch if predicate(item))
        if len(batch) < per_page:
            break
        page += 1

    return matches[:desired_count]


def main():
    args = parse_args()
    repository_id = f"{args.owner}/{args.repo}"
    client = GitHubClient(args.owner, args.repo)

    repository_info = client.get_json("")
    data = {
        "repository": {
            "id": repository_id,
            "name": repository_info.get("name") or args.repo,
            "url": repository_info.get("html_url"),
            "source_url": repository_info.get("html_url"),
        },
        "commits": [],
        "pull_requests": [],
        "issues": [],
    }

    commits_by_sha = {}
    issues_by_id = {}

    print(f"Fetching public GitHub history for {repository_id}...")

    # Fetch a useful recent commit window. The list endpoint supplies commit
    # metadata; details are requested only for the configured number of commits
    # so the script stays within the unauthenticated API budget.
    commit_summaries = client.get_json(
        "/commits",
        {"per_page": max(args.commits, 1), "page": 1},
    ) if args.commits else []

    for item in commit_summaries[:args.commits]:
        add_commit(item, repository_id, commits_by_sha)

    detail_count = min(args.commit_details, len(commit_summaries))
    for item in commit_summaries[:detail_count]:
        detailed = client.get_json(f"/commits/{item['sha']}")
        record = add_commit(detailed, repository_id, commits_by_sha)
        record["files"] = [
            changed_file["filename"]
            for changed_file in detailed.get("files", [])
            if changed_file.get("filename")
        ]

    # Only merged PRs are useful evidence of changes that entered the repo.
    pull_requests = fetch_matching(
        client,
        "/pulls",
        {"state": "closed", "sort": "updated", "direction": "desc"},
        args.pull_requests,
        lambda pull_request: bool(pull_request.get("merged_at")),
    )

    closing_issue_pattern = re.compile(
        r"(?i)\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+#(\d+)\b"
    )
    linked_issue_numbers = []

    for pull_request in pull_requests:
        pull_request_id = f"{repository_id}#{pull_request['number']}"
        commit_summaries = client.get_json(
            f"/pulls/{pull_request['number']}/commits",
            {"per_page": MAX_PAGE_SIZE, "page": 1},
        )
        commit_ids = []

        for item in commit_summaries:
            commit = add_commit(
                item,
                repository_id,
                commits_by_sha,
                pull_request_id=pull_request_id,
            )
            if commit["id"] not in commit_ids:
                commit_ids.append(commit["id"])

        body = pull_request.get("body") or ""
        issue_numbers = list(dict.fromkeys(
            int(number) for number in closing_issue_pattern.findall(body)
        ))
        linked_issue_numbers.extend(issue_numbers)

        data["pull_requests"].append({
            "id": pull_request_id,
            "number": pull_request["number"],
            "title": pull_request.get("title") or "",
            "body": body[:BODY_LIMIT],
            "author_login": author_login(pull_request),
            "created_at": pull_request.get("created_at"),
            "merged_at": pull_request.get("merged_at"),
            "url": pull_request.get("html_url"),
            "source_url": pull_request.get("html_url"),
            "commit_ids": commit_ids,
            "issue_ids": [],
            "closing_issue_numbers": issue_numbers,
        })

    # Issues endpoint also returns PRs, so exclude records carrying pull_request.
    issue_summaries = fetch_matching(
        client,
        "/issues",
        {"state": "all", "sort": "updated", "direction": "desc"},
        args.issues,
        lambda issue: not issue.get("pull_request"),
    )
    for issue in issue_summaries:
        record = make_issue(issue, repository_id)
        issues_by_id[record["id"]] = record

    # Fetch only a bounded number of linked issues missing from the recent issue
    # window. These are the explicit GitHub closing references in PR bodies.
    remaining_link_fetches = args.linked_issue_details
    for number in dict.fromkeys(linked_issue_numbers):
        issue_id = f"{repository_id}#{number}"
        if issue_id in issues_by_id:
            continue
        if remaining_link_fetches <= 0:
            break

        issue = client.get_json(f"/issues/{number}")
        remaining_link_fetches -= 1
        if not issue.get("pull_request"):
            record = make_issue(issue, repository_id)
            issues_by_id[record["id"]] = record

    for pull_request in data["pull_requests"]:
        for number in pull_request.pop("closing_issue_numbers"):
            issue_id = f"{repository_id}#{number}"
            if issue_id in issues_by_id and issue_id not in pull_request["issue_ids"]:
                pull_request["issue_ids"].append(issue_id)

    data["commits"] = list(commits_by_sha.values())
    data["issues"] = list(issues_by_id.values())

    if args.output:
        output_path = Path(args.output).expanduser()
    else:
        filename = f"{args.owner}_{args.repo}_final.json".replace("/", "_")
        output_path = Path(__file__).parent / "data" / filename
    if not output_path.is_absolute():
        output_path = Path(__file__).parent / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)

    detailed_commit_count = sum(bool(commit["files"]) for commit in data["commits"])
    print(f"Saved normalized final dataset to: {output_path}")
    print(
        f"Repository: {repository_id} | Commits: {len(data['commits'])} "
        f"({detailed_commit_count} with changed-file details) | "
        f"Merged pull requests: {len(data['pull_requests'])} | "
        f"Issues: {len(data['issues'])} | API requests: {client.request_count}"
    )
    if not client.token:
        print("Using GitHub's public unauthenticated API; no paid service is involved.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, KeyError, ValueError) as error:
        raise SystemExit(f"Ingestion stopped: {error}") from error
