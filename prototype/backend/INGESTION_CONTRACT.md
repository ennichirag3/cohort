# GitHub Ingestion Contract

Shreya's ingestion pipeline provides normalized repository data to the Neo4j loader.
Preserve GitHub IDs, timestamps, and source URLs. Missing optional values should be
null or an empty list, not invented.

## Stable IDs

- Repository: `owner/repo`
- Commit: `owner/repo@<full-commit-sha>`
- Pull request: `owner/repo#<number>`
- Issue: `owner/repo#<number>`
- Developer: `github:<login>`
- File: `owner/repo:<path>`

## Record fields

### Repository
`id`, `name`, `url`

### Commit
`id`, `sha`, `message`, `author_login`, `committed_at`, `url`,
`files` (list of paths), `pull_request_ids` (list of PR IDs)

### Pull request
`id`, `number`, `title`, `body`, `author_login`, `created_at`,
`merged_at`, `url`, `commit_ids` (list of commit IDs),
`issue_ids` (list of issue IDs)

### Issue
`id`, `number`, `title`, `body`, `author_login`, `created_at`,
`updated_at`, `url`
