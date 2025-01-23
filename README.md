# GitHub Branch Protector

Automate and verify branch protection rules across multiple GitHub repositories. This tool helps maintain consistent security practices by enforcing and verifying branch protection rules on default branches.

## Features

- 🔒 Automated branch protection rule deployment
- ✅ Verification-first approach (only applies changes when needed)
- 🎯 Automatic default branch detection
- 📊 Detailed PDF reports of protection status
- 🔄 Batch processing of multiple repositories
- 📝 Detailed logging
- 📋 Support for repository lists via file or command line
- ⚙️ Configurable via environment variables

## Branch Protection Rules

The tool enforces and verifies the following protection rules:
- Required pull request reviews (minimum 1 reviewer)
- Required status checks
- Admin enforcement enabled
- Force pushes disabled
- Branch deletions disabled
- Linear history required

## Usage as GitHub Action

Add this workflow to your repository:

```yaml
name: Branch Protection Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:
    inputs:
      verify_only:
        description: 'Only verify protection rules'
        type: boolean
        default: true

jobs:
  protect-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Branch Protection
        uses: radioactivetobi/github-branch-protector@v1
        env:
          BRANCH_PROTECTION_ACTION: ${{ secrets.BRANCH_PROTECTION_ACTION }}
        with:
          github_token: ${{ secrets.BRANCH_PROTECTION_ACTION }}
          github_owner: ${{ github.repository_owner }}
          repositories: "repo1 repo2 repo3"
          verify_only: ${{ github.event.inputs.verify_only }}
```

### Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github_token` | GitHub token with repository access | Yes | - |
| `github_owner` | GitHub organization or username | Yes | - |
| `repositories` | Space-separated list of repositories | Yes | - |
| `verify_only` | Only verify protection rules | No | false |

## Local Installation

1. Clone the repository:
```bash
git clone https://github.com/radioactivetobi/github-branch-protector.git
cd github-branch-protector
```

2. Create and activate a virtual environment:
```