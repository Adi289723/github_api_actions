import os
import subprocess
from datetime import datetime

def create_github_workflow():
    """Create and deploy GitHub Actions workflow for daily commits."""
    
    # Workflow content
    workflow_content = """name: Daily Commit Workflow

on:
  schedule:
    - cron: '30 18 * * *'  # 12:00 AM IST
  workflow_dispatch:

jobs:
  daily-commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Configure Git with email 21f3002781@ds.study.iitm.ac.in
        run: |
          git config user.name "DevSync Bot"
          git config user.email "21f3002781@ds.study.iitm.ac.in"
      
      - name: Create daily update
        run: |
          mkdir -p logs
          echo "Daily update: $(date '+%Y-%m-%d %H:%M:%S UTC')" >> logs/daily-updates.txt
          echo "Workflow run: ${{ github.run_number }}" >> logs/daily-updates.txt
          echo "---" >> logs/daily-updates.txt
      
      - name: Commit and push changes
        run: |
          git add .
          git commit -m "chore: daily automated update $(date '+%Y-%m-%d')"
          git push
"""
    
    # Create directory structure
    os.makedirs('.github/workflows', exist_ok=True)
    
    # Write workflow file
    workflow_path = '.github/workflows/daily-commit.yml'
    with open(workflow_path, 'w') as f:
        f.write(workflow_content)
    
    print(f"✓ Created workflow file: {workflow_path}")
    
    # Git operations
    try:
        subprocess.run(['git', 'add', workflow_path], check=True)
        subprocess.run(['git', 'commit', '-m', 'Add daily commit GitHub Actions workflow'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("✓ Workflow committed and pushed to GitHub")
    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
        return False
    
    return True

def trigger_workflow():
    """Manually trigger the workflow using GitHub CLI."""
    try:
        result = subprocess.run(
            ['gh', 'workflow', 'run', 'daily-commit.yml'],
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ Workflow triggered successfully")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error triggering workflow: {e}")
        print("You can manually trigger it from GitHub Actions page")
        return False
    except FileNotFoundError:
        print("GitHub CLI not found. Install it or trigger manually from GitHub web interface")
        return False

def get_repo_url():
    """Get the current repository URL."""
    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            check=True,
            capture_output=True,
            text=True
        )
        url = result.stdout.strip()
        # Convert SSH to HTTPS format if needed
        if url.startswith('git@github.com:'):
            url = url.replace('git@github.com:', 'https://github.com/')
            url = url.replace('.git', '')
        return url
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    print("Creating GitHub Actions workflow for daily commits...")
    print("=" * 60)
    
    if create_github_workflow():
        print("\n" + "=" * 60)
        print("Attempting to trigger workflow...")
        trigger_workflow()
        
        print("\n" + "=" * 60)
        repo_url = get_repo_url()
        if repo_url:
            print(f"\nRepository URL: {repo_url}")
            print(f"Actions page: {repo_url}/actions")
        
        print("\n" + "=" * 60)
        print("Next steps:")
        print("1. Go to your repository's Actions tab")
        print("2. Click on 'Daily Commit Workflow'")
        print("3. Click 'Run workflow' to test it")
        print("4. Verify the commit is created within 5 minutes")
