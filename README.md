# GitHub Branch Protection Automation

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
        uses: radioactivetobi/github-branch-protection@v1
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
git clone https://github.com/radioactivetobi/github-branch-protection.git
cd github-branch-protection
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Local Usage

```bash
# Verify protection rules without making changes
python -m src.main --verify-only --repos repo1 repo2 repo3

# Apply protection rules where needed
python -m src.main --repos repo1 repo2 repo3

# Using repository list file
python -m src.main --repos-file repos.txt
```

### Repository List File Format

Create a text file (e.g., `repos.txt`):
```text
# One repository per line
repo1
repo2
repo3
```

## Environment Variables

Create a `.env` file with your settings:
```env
GITHUB_TOKEN=your_token_here
GITHUB_OWNER=your_org_or_username
REPOSITORIES=repo1 repo2 repo3  # Optional, can use command line args instead
VERIFY_ONLY=false              # Optional, defaults to false
```

## Generated Reports

The tool generates detailed PDF reports containing:
- Protection status summary
- Repository-specific results
- Detailed issues found (if any)
- Verification timestamps

Reports are saved in the `reports` directory:
```
reports/branch_protection_report_YYYYMMDD_HHMMSS.pdf
```

## Verification Process

1. **Initial Check**
   - Verifies existing protection rules
   - Identifies missing or incorrect settings
   - Logs detailed status information

2. **Application (if needed)**
   - Only applies changes if verification fails
   - Updates protection rules to meet requirements
   - Maintains existing compliant settings

3. **Final Verification**
   - Confirms applied changes
   - Generates detailed report
   - Provides actionable feedback

## Required Permissions

The GitHub token needs:
- `repo` scope for private repositories
- `public_repo` scope for public repositories
- Admin access to target repositories

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify token permissions
   - Check token expiration
   - Ensure correct environment variables

2. **Repository Access Issues**
   - Confirm admin access
   - Verify repository names
   - Check organization membership

3. **Protection Rule Errors**
   - Review repository settings
   - Check branch existence
   - Verify token permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
