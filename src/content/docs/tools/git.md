---
title: Git
description: Git.
---

```bash
# Installation
sudo apt-get install git  # or sudo apt install git
git --version

# Global Config
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com
git config --global core.editor "code --wait"
# Open global Git configuration file in default editor for modification
git config --global -e

# Add server's SSH key to known_hosts file to enable secure connection
# The known_hosts file stores SSH server public keys for verification
# When connecting to a server for the first time, SSH checks if the server's key is in known_hosts
# If not found, SSH prompts to verify and add the key to prevent man-in-the-middle attacks
# ssh-keyscan retrieves the server's public key
# -p: specify port number
# ${SERVER}: server hostname or IP address
ssh-keyscan -p ${PORT} ${SERVER} >> $HOME/.ssh/known_hosts

# Gerrit Workflow
git clone <git_url> <target_dir>
git remote set-url --push origin <git_url>
git config remote.origin.push HEAD:refs/for/master
mv .git/hooks/ .git/hooks.bak
mkdir --parents .git/hooks
git clone "<git_url>/git-hooks" .git/hooks
scp -P 29418 "<remote_url>:hooks/commit-msg" ".git/hooks"

git fetch
git rebase --committer-date-is-author-date origin/master feature_branch
git push origin feature_branch:refs/for/master

# Fetch latest info before listing (get the newly created branches on the remote)
git fetch --all

# List all branches that have been merged into the current branch
git branch --merged

# Delete a local branch
git branch -d <branch-name> || git branch -D <branch-name>

# List all remote branches
git branch -r

# List all local and remote branches
git branch -a

# Delete a remote branch
git push origin --delete <branch-name>
git push origin :<branch-name>

#  removes any remote-tracking branches that no longer exist on the remote
# Fetch updates from remote and prune deleted branches
# --prune removes remote-tracking references that no longer exist on the remote
# --prune-tags also removes deleted tags (added in Git 2.17+)
git fetch --prune --prune-tags
```

## GitHub

### Remove all the runs in a workflow via `gh`
```bash
org=org_name
repo=repo_name
WORKFLOW_NAME="workflow.yml"

# List all workflows in the specified repository
gh workflow list --repo "${org}/${repo}"

# List all runs for a specific workflow in the repository
gh run list --workflow "$WORKFLOW_NAME_OR_ID" --repo "$org/$repo"

# Get all workflow run IDs
RUN_IDS=$(gh run list --workflow "$WORKFLOW_NAME" --repo "$org/$repo" --json databaseId --jq '.[].databaseId')

# Loop through each run ID and delete it
for RUN_ID in $RUN_IDS; do
  echo "Deleting run $RUN_ID..."
  gh api \
    --method DELETE \
    -H "Accept: application/vnd.github+json" \
    "/repos/$org/$repo/actions/runs/$RUN_ID"
done

echo "All runs deleted."
```

## Open Source Contribution
The following is the example of Django
```bash
# First fork project on GitHub.

# Download src
git clone https://github.com/YourGitHubName/django.git
# --depth 1 to skip downloading all the commit history

# Create venv
python3 -m venv ~/.virtualenvs/djangodev
source ~/.virtualenvs/djangodev/bin/activate

# Install the copy in the editable mode
# You will immediately see any changes you make to it
python -m pip install -e /path/to/your/local/clone/django/

# Creating projects with a local copy of Django
# Running Django’s test suite for the first time

# Working on a feature
git checkout -b ticket_99999

# Writing some tests for your ticket
# For bug fix contributions, writing a regression test
# A good way to do this is to write your new tests first, before making any changes to the code. This style of development is called test-driven development and can be applied to both entire projects and single changes.

# Running your new test

# Writing the code for your ticket

# Running new test

# it’s a good idea to run the entire Django test suite to verify that your change hasn’t introduced any bugs into other areas of Django

# Writing Documentation
# function docs and add to the release notes

# Stage changes
git add --all

# display the diff
git diff --cached

# commit
git commit
# msg: Fixed #99999 -- Added a shortcut function to make toast.

# Pushing the commit and making a pull request
# send it to your fork on GitHub
git push origin ticket_99999

# create a pull request by visiting the Django GitHub page
```
