# GitHub Branch Protection Automation

Automate the deployment and management of branch protection rules across multiple GitHub repositories. This tool helps maintain consistent security practices by enforcing branch protection rules on default branches, including:

- Required pull request reviews
- Status check requirements
- Admin enforcement
- Force push restrictions
- Branch deletion restrictions

## Features

- 🔒 Automated branch protection rule deployment
- 🎯 Automatic default branch detection
- 📊 Detailed PDF reports of protection status
- 🔄 Batch processing of multiple repositories
- 📝 Detailed logging
- 📋 Support for repository lists via file input
- ⚙️ Configurable via environment variables or command line
- 🛡️ Error handling and retry logic

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/radioactivetobi/github-branch-protection.git
cd github-branch-protection
```

2. Copy and configure the environment file:
```bash
cp .env.example .env
# Edit .env with your GitHub settings
```

3. Run with Docker Compose:
```bash
docker-compose up
```

## Alternative Installation (without Docker)

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `.env` with your settings:
```env
# GitHub Personal Access Token with repo scope
GITHUB_TOKEN=your_token_here

# GitHub Organization or Username
GITHUB_OWNER=your_org_or_username

# Comma-separated list of repository names (optional if using --repos or --repos-file)
REPOSITORIES=repo1,repo2,repo3

# Logging
LOG_LEVEL=INFO
```

### Repository List File Format

Create a text file (e.g., `repos.txt`) with repository names:
```text
# List your repositories below (one per line)
# Lines starting with # are ignored
repo1
repo2
repo3
```

### GitHub Token Permissions

Your GitHub token needs the following permissions:
- `repo` scope for private repositories
- `public_repo` scope for public repositories

Generate a token at: https://github.com/settings/tokens

## Usage

### Local Usage

```bash
# Basic usage
python -m src.main

# Verify mode (check without modifying)
python -m src.main --verify-only

# Using repository list file
python -m src.main --verify-only --repos-file repos.txt

# Specific repositories via command line
python -m src.main --repos repo1 repo2 repo3
```

### GitHub Actions Usage

You can use this tool as a GitHub Action in your workflows. There are two ways to use it:

#### 1. Using the Pre-built Action

```yaml
name: Branch Protection Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Run weekly on Monday
  workflow_dispatch:
    inputs:
      verify_only:
        description: 'Only verify protection rules'
        type: boolean
        default: false

jobs:
  protect-branches:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run branch protection
        uses: your-username/github-branch-protection@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_owner: ${{ github.repository_owner }}
          repos_file: 'repos.txt'
          verify_only: ${{ github.event.inputs.verify_only }}
```

#### 2. Using the Composite Action

```yaml
name: Branch Protection Check

on:
  workflow_dispatch:

jobs:
  protect-branches:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: ./.github/actions/branch-protection
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_owner: ${{ github.repository_owner }}
          repos_file: 'repos.txt'
```

### Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github_token` | GitHub token with repository access | Yes | - |
| `github_owner` | GitHub organization or username | Yes | - |
| `repos_file` | Path to file containing repository names | No | - |
| `repos` | Space-separated list of repositories | No | - |
| `verify_only` | Only verify protection rules without modifying | No | false |

### Workflow Triggers

The action can be triggered in several ways:
- **Schedule**: Run automatically on a defined schedule
- **Manual**: Trigger manually through the GitHub UI
- **Other Events**: Can be integrated with other GitHub events like push or pull request

### Action Artifacts

The action automatically uploads the generated PDF report as a workflow artifact:
- Report name: `branch-protection-report`
- Retention period: 30 days
- Contains detailed analysis of protection rules

## Generated Reports

The tool generates detailed PDF reports containing:
- Executive summary with compliance statistics
- Detailed results for each repository
- Status of protection rules
- Issues found (if any)
- Recommendations for optimal security

Reports are saved in the `reports` directory with timestamps:
```
reports/branch_protection_report_YYYYMMDD_HHMMSS.pdf
```

## Branch Protection Rules

The tool enforces the following protection rules on the default branch:

- **Pull Request Reviews**
  - Requires 1 approving review
  - Dismisses stale pull request approvals
  - Restricts review dismissals

- **Status Checks**
  - Requires status checks to pass
  - Requires branches to be up to date

- **Additional Protections**
  - Enforces for administrators
  - Prevents force pushes
  - Prevents branch deletions
  - Requires strict status checks

## Example Output

```
2024-XX-XX XX:XX:XX - INFO - Connected to GitHub as username
2024-XX-XX XX:XX:XX - INFO - Starting branch protection automation
2024-XX-XX XX:XX:XX - INFO - Loaded 3 repositories from repos.txt
2024-XX-XX XX:XX:XX - INFO - Processing repositories: repo1, repo2, repo3
2024-XX-XX XX:XX:XX - INFO - Default branch is: main
2024-XX-XX XX:XX:XX - INFO - Setting branch protection ruleset for repo1
2024-XX-XX XX:XX:XX - INFO - Successfully set branch protection for repo1
2024-XX-XX XX:XX:XX - INFO - Generated protection report: reports/branch_protection_report_20240320_143022.pdf
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your GitHub token has the required permissions
   - Check that the token hasn't expired
   - Ensure the token is correctly set in .env

2. **Repository Access Issues**
   - Confirm you have admin access to the repositories
   - Verify repository names are correct
   - Check organization membership if using org repositories

3. **Rate Limiting**
   - The tool includes automatic delay between operations
   - Check GitHub API rate limits if processing many repositories

4. **File Input Issues**
   - Ensure the repository list file exists
   - Check file permissions
   - Verify file format (one repository per line)
   - Remove any special characters or BOM markers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## GitHub Action Development

If you want to modify the action:

1. Action files are located in `.github/actions/branch-protection/`
2. Main workflow file is in `.github/workflows/branch-protection.yml`
3. The action can be used either as a Docker container or composite action

### Action Files Structure
```
.github/
├── actions/
│   └── branch-protection/
│       ├── action.yml          # Docker-based action
│       └── composite-action.yml # Composite action
└── workflows/
    └── branch-protection.yml   # Example workflow
```

### Building the Action Locally

```bash
# Build the Docker image
docker build -t branch-protection .

# Run the action locally
docker run -e GITHUB_TOKEN=your_token \
          -e GITHUB_OWNER=your_username \
          branch-protection --verify-only
```
