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
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Branch Protection
        uses: radioactivetobi/github-branch-protection@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          github_owner: ${{ github.repository_owner }}
          repos: "repo1 repo2 repo3"
          verify_only: ${{ github.event.inputs.verify_only }}
```

### Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github_token` | GitHub token with repository access | Yes | - |
| `github_owner` | GitHub organization or username | Yes | - |
| `repos` | Space-separated list of repositories | No | - |
| `repos_file` | Path to file containing repository names | No | - |
| `verify_only` | Only verify protection rules | No | false |

### Repository List File Format

If using `repos_file`, create a text file (e.g., `repos.txt`):
```text
# One repository per line
repo1
repo2
repo3
```

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
# Basic usage
python -m src.main

# Verify mode (check without modifying)
python -m src.main --verify-only

# Using repository list file
python -m src.main --verify-only --repos-file repos.txt

# Specific repositories via command line
python -m src.main --repos repo1 repo2 repo3
```

## Docker Usage

1. Build the image:
```bash
docker build -t branch-protection .
```

2. Run the container:
```bash
docker run -e GITHUB_TOKEN=your_token \
          -e GITHUB_OWNER=your_username \
          branch-protection --verify-only
```

## Configuration

Create a `.env` file with your settings:
```env
GITHUB_TOKEN=your_token_here
GITHUB_OWNER=your_org_or_username
```

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

The tool enforces the following protection rules:
- Required pull request reviews
- Required status checks
- Enforce for administrators
- Prevent force pushes
- Prevent branch deletions

## Project Structure
```
.
├── .github/
│   ├── actions/
│   │   └── branch-protection/
│   │       └── action.yml
│   └── workflows/
│       └── branch-protection.yml
├── src/
│   ├── __init__.py
│   ├── github_api.py
│   ├── config.py
│   ├── logger.py
│   ├── main.py
│   └── report_generator.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── entrypoint.sh
├── LICENSE
├── README.md
├── repos.txt.example
└── requirements.txt
```

## Required Permissions

The `GITHUB_TOKEN` needs:
- `repo` scope for private repositories
- `public_repo` scope for public repositories

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your GitHub token has required permissions
   - Check token expiration
   - Ensure token is correctly set

2. **Repository Access Issues**
   - Confirm admin access to repositories
   - Verify repository names
   - Check organization membership

3. **Action Execution Issues**
   - Ensure workflow has correct permissions
   - Verify input parameters
   - Check repository structure matches requirements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
