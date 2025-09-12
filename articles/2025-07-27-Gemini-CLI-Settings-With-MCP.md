# Gemini CLI settings.json with MCP Config

Here is a sample settings.json file for the Gemini CLI, configured with the Git and GitHub MCP servers.

Put this into `~/.gemini/settings.json`:
{
  "selectedAuthType": "gemini-api-key",
  "theme": "Dracula",
  "preferredEditor": "vscode",
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": [
        "mcp-server-git"
      ]
    },
    "github": {
      "httpUrl": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "<your GitHub Personal Access Token here>"
      },
      "timeout": 5000
    }
  }
}
## Getting a GitHub Personal Access Token

Go to https://github.com/settings/tokens and generate a token with the scopes you need. 

Then paste it into settings.json.

Note: I had hoped to get the token from an environment variable, but the Gemini CLI does not support that as far as I can tell from the documentation.

## Verifying that the MCP Servers Work

In Gemini CLI, run `/mcp`. You should see a list of all the tools Gemini CLI now has access to, from each MCP server.

If you have your settings.json in the right location and your GitHub PAT set correctly, you should see something like:
╭──────────╮
│  > /mcp  │
╰──────────╯


ℹ Configured MCP servers:

  🟢 git - Ready (13 tools)
    - git_add
    - git_branch
    - git_checkout
    - git_commit
    - git_create_branch
    - git_diff
    - git_diff_staged
    - git_diff_unstaged
    - git_init
    - git_log
    - git_reset
    - git_show
    - git_status

  🟢 github - Ready (74 tools)
    - add_comment_to_pending_review
    - add_issue_comment
    - assign_copilot_to_issue
    - cancel_workflow_run
    - create_and_submit_pull_request_review
    - create_branch
    - create_issue
    - create_or_update_file
    - create_pending_pull_request_review
    - create_pull_request
    - create_pull_request_with_copilot
    - create_repository
    - delete_file
    - delete_pending_pull_request_review
    - delete_workflow_run_logs
    - dismiss_notification
    - download_workflow_run_artifact
    - fork_repository
    - get_code_scanning_alert
    - get_commit
    - get_dependabot_alert
    - get_discussion
    - get_discussion_comments
    - get_file_contents
    - get_issue
    - get_issue_comments
    - get_job_logs
    - get_me
    - get_notification_details
    - get_pull_request
    - get_pull_request_comments
    - get_pull_request_diff
    - get_pull_request_files
    - get_pull_request_reviews
    - get_pull_request_status
    - get_secret_scanning_alert
    - get_tag
    - get_workflow_run
    - get_workflow_run_logs
    - get_workflow_run_usage
    - list_branches
    - list_code_scanning_alerts
    - list_commits
    - list_dependabot_alerts
    - list_discussion_categories
    - list_discussions
    - list_issues
    - list_notifications
    - list_pull_requests
    - list_secret_scanning_alerts
    - list_tags
    - list_workflow_jobs
    - list_workflow_run_artifacts
    - list_workflow_runs
    - list_workflows
    - manage_notification_subscription
    - manage_repository_notification_subscription
    - mark_all_notifications_read
    - merge_pull_request
    - push_files
    - request_copilot_review
    - rerun_failed_jobs
    - rerun_workflow_run
    - run_workflow
    - search_code
    - search_issues
    - search_orgs
    - search_pull_requests
    - search_repositories
    - search_users
    - submit_pending_pull_request_review
    - update_issue
    - update_pull_request
    - update_pull_request_branch
## Using the Git and GitHub MCP Tools from Gemini CLI

Just those two MCP servers give you a lot of useful things you can do.

You can prompt things like this:
╭──────────────────────────────────────────────────────────────────────────────────────────────╮
│  > Fill out the description of https://github.com/audreyfeldroy/audrey.feldroy.com/issues/8  │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯