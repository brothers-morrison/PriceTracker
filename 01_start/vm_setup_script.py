#!/usr/bin/env python3
"""
VM Setup Script for Ralph-Loop Project

Converts the original bash setup script to Python for better maintainability
and cross-platform compatibility.

TODO:
- Upgrade to use Terraform instead of manual setup
- Explore CI/CD options (GitHub Actions, etc.)
- Automate GitHub CLI authentication
- Fix SSH key addition via gh CLI
"""

import subprocess
import sys
import os
from typing import Optional, Union, List
from pathlib import Path



"""
# Source - https://stackoverflow.com/a/287944
# Posted by joeld, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-21, License - CC BY-SA 4.0
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CommandRunner:
    """Utility class for running shell commands."""
    
    @staticmethod
    def run(
        command: Union[str, List[str]],
        shell: bool = True,
        capture: bool = True,
        check: bool = True,
        cwd: Optional[str] = None,
        env: Optional[dict] = None,
        timeout: Optional[int] = None
    ) -> subprocess.CompletedProcess:
        """
        Execute a shell command and return the result.
        
        Args:
            command: Command to execute (string if shell=True, list otherwise)
            shell: Whether to run command through shell
            capture: Whether to capture stdout/stderr
            check: Whether to raise exception on non-zero exit
            cwd: Working directory for command
            env: Environment variables
            timeout: Timeout in seconds
        
        Returns:
            CompletedProcess object with stdout, stderr, returncode
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=capture,
                text=True,
                check=check,
                cwd=cwd,
                env=env,
                timeout=timeout
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
            print(f"stdout: {e.stdout}", file=sys.stderr)
            print(f"stderr: {e.stderr}", file=sys.stderr)
            raise
        except subprocess.TimeoutExpired as e:
            print(f"Command timed out after {timeout} seconds", file=sys.stderr)
            raise
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            raise
            
    @staticmethod        
    def write_file_and_execute(filename, contents):
        file_to_exec= Path(filename)
        # Write out the github commands above, too painful to try to convert to python calls...
        with open(file_to_exec, 'w') as f:
            f.write(contents)
        
        # make it executable on linux
        os.system(f'sudo chmod +x {str(file_to_exec)}')
        os.system(f'exec {str(file_to_exec)}')
        # TBD: validate that this worked... validate file exists, not empty
        # TBD: validate something that would only be there if it succeeded
        # When finished, clean up the file
        file_to_exec.unlink()


class VMSetup:
    """Main setup class for configuring VM for Ralph-Loop."""
    
    def __init__(self, github_repo: str, email: str, api_key: str, project_repo: str = ""):
        self.github_repo = github_repo
        self.project_repo = project_repo
        self.email = email
        self.api_key = api_key
        self.runner = CommandRunner()
        
    def color(self, message: str):
        print(f"\n{bcolors.OKGREEN}{message}{bcolors.ENDC}\n")
        
    def h1(self, message: str, decorative_char='=', line_length=40):
        """Print a formatted section header."""
        print(f"\n{bcolors.OKGREEN}{decorative_char*line_length}{bcolors.ENDC}")
        print(f"  {message}")
        print(f"{bcolors.OKGREEN}{decorative_char*line_length}{bcolors.ENDC}\n")
    
    def h2(self, message: str, decorative_char='=', line_length=40):
        print(f"\n{decorative_char*line_length}  {message}  {decorative_char*line_length}\n")
    
    def clone_and_configure_git(self):
        """Clone repository and configure Git settings."""
        self.h1("Cloning Repository and Configuring Git")
        
        print("NOTE: GitHub Personal Access Tokens (PAT) can only be used with HTTPS, not SSH")
        print("See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens")
        
        # Clone repository
        print(f"\nCloning repository: {self.github_repo}")
        self.runner.run(['git', 'clone', self.github_repo])
        
        # Configure Git globally
        print("\nConfiguring Git user settings...")
        self.runner.run(['git', 'config', '--global', 'user.email', self.email])
        self.runner.run(['git', 'config', '--global', 'user.name', 'Ralph Wiggum'])
        
        print("✓ Git configuration complete")
    
    def setup_nodejs(self):
        """Install Node.js and npm."""
        self.h1("Installing Node.js")
        
        
        
        # Install Node.js
        print("Installing Node.js 20.x...")
        self.runner.run(
            'curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -',
            shell=True
        )
        os.system('sudo apt install -y nodejs')
        
        # Verify installation
        result = self.runner.run(['node', '--version'])
        print(f"✓ Node.js installed: {result.stdout.strip()}")
        
        result = self.runner.run(['npm', '--version'])
        print(f"✓ npm installed: {result.stdout.strip()}")
    
    def setup_api_key(self):
        """Configure OpenRouter API key.
        Is this a necessary step???
        """
        self.h1("Setting Up API Key")
        
        print("Setting OPENROUTER_API_KEY environment variable...")
        os.environ['OPENROUTER_API_KEY'] = self.api_key
        
        # Add to .bashrc for persistence
        bashrc_path = Path.home() / '.bashrc'
        export_line = f'export OPENROUTER_API_KEY="{self.api_key}"\n'
        
        with open(bashrc_path, 'a') as f:
            f.write(f'\n# Added by VM setup script\n{export_line}')
        
        print("✓ API key configured and added to .bashrc")
    
    def setup_playwright(self):
        """Install Playwright and its dependencies."""
        self.h1("Installing Playwright")
        
        print("Installing Playwright dependencies...")
        self.runner.run(['npx', 'playwright', 'install-deps'])
        
        print("Installing Playwright browsers...")
        self.runner.run(['npx', 'playwright', 'install'])
        
        print("✓ Playwright installation complete")
    
    def setup_github_cli(self):
        """Install and configure GitHub CLI."""
        self.h1("Setting Up GitHub CLI")
        
        
        print("# taken from https://gist.github.com/Manoj-Paramsetti/dc957bdd6a4430275d0fc28a0dc43ae9#official-sources")
        
        print("WTF Github, why is this so complicated... ?")
        print("https://github.com/cli/cli/blob/trunk/docs/install_linux.md#debian-ubuntu-linux-raspberry-pi-os-apt\n\n")
        setup_github_contents='''
        # https://github.com/cli/cli/blob/trunk/docs/install_linux.md#debian-ubuntu-linux-raspberry-pi-os-apt
(type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
	&& sudo mkdir -p -m 755 /etc/apt/keyrings \
	&& out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
	&& cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
	&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
	&& sudo mkdir -p -m 755 /etc/apt/sources.list.d \
	&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
	&& sudo apt update \
	&& sudo apt install gh -y
        '''
        self.runner.write_file_and_execute('setup_github.sh', setup_github_contents)
        # TBD: validate that this worked... validate file exists, not empty
        # TBD: validate something that would only be there if it succeeded
        
        print("Installing GitHub CLI...")
        os.system(f'sudo apt install -y gh')
        
        self.h1("  MANUAL STEP REQUIRED: GitHub CLI Authentication")
        print("\nPlease run the following command manually and follow the prompts:")
        self.color("  gh auth login")
        print("\nThis will authenticate you with GitHub interactively.")
        print("TODO: Explore automation options for this step\n")
        os.system("gh auth login")
    
    def setup_ssh_keys(self):
        """Generate SSH keys for GitHub."""
        self.h1("Setting Up SSH Keys")
        
        ssh_key_path = Path.home() / '.ssh' / 'id_ed25519'
        
        do_generate_key = True
        if ssh_key_path.exists():
            print(f"SSH key already exists at {ssh_key_path}")
            response = input("Do you want to overwrite it? (y/N): ")
            if response.lower() != 'y':
                print("Skipping SSH key generation")
                do_generate_key = False
        
        if(do_generate_key):
            self.h1(f"Generating SSH key with email: {self.email}")
            self.h2("MANUAL STEP: You will be prompted for a passphrase")
            
            try:
                self.runner.run(
                    ['ssh-keygen', '-t', 'ed25519', '-C', self.email],
                    capture=False  # Let user see prompts
                )
            except subprocess.CalledProcessError:
                print("SSH key generation was cancelled or failed")
                return
        
        
        
        pub_key_path = Path(str(ssh_key_path) + '.pub')        
        if pub_key_path.exists():
            with open(pub_key_path, 'r') as f:
                pub_key = f.read().strip()
            
            self.h1("SSH Public Key Generated")
            print(f"\nYour public key:\n{bcolors.OKBLUE}{pub_key}{bcolors.ENDC}\n")
            print("Please add this key to your GitHub account:")
            print("  https://github.com/settings/keys\n\n")
            
            
            print("We'll wait while you now paste your SSH key into GitHub CLI...")
            os.system('sleep 3s')
            #print("\nNote: The 'gh ssh-key add' command currently fails with:")
            #print("  'HTTP 403: Resource not accessible by personal access token'")
            #print("TODO: adjust git remote to use SSH rather than HTTPS when performing git clone \n")
        else:
            print("SSH key file not found after generation")
    
    def sync_repository(self, repo_name: str):
        """Fetch, pull, and push repository changes."""
        self.h1("Syncing Repository")
        
        repo_path = Path(repo_name)
        if not repo_path.exists():
            print(f"Repository directory '{repo_name}' not found")
            return
        
        print(f"Working in repository: {repo_path}")
        
        # Fetch updates
        print("Fetching from remote...")
        self.runner.run(['git', 'fetch'], cwd=str(repo_path))
        
        # Pull changes
        print("Pulling changes...")
        try:
            self.runner.run(['git', 'pull'], cwd=str(repo_path))
        except subprocess.CalledProcessError as e:
            print(f"Warning: git pull failed: {e}")
        
        # Push changes
        print("Pushing to remote...")
        try:
            self.runner.run(
                ['git', 'push', '--set-upstream', 'origin', 'main'],
                cwd=str(repo_path)
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: git push failed: {e}")
            print("You may need to authenticate or set up the remote properly")
    
    
    def user_bash_files(self):
        bash_aliases_contents='''
        # Using tool: https://docs.ntfy.sh/
        # Login to https://ntfy.sh/aider_ralph_01_alerts receive alerts in browser
NTFY_TOPIC="aider_ralph_01_alerts"


random_gen() {
        # Seed random generator
        random="${1:-`$$$(date +%N)`}"
        echo $random
}

ralph_quote() {
        # Seed random generator
        random="${1:-`echo $$$(date +%N)`}"
        quotes=(
                "I bent my wookie..."
                "Oh boy! Sleep! That's when I'm a Viking!"
                "Will you be my mommy? You smell like dead bunnies."
                "I eated the purple berries!"
                "I dropped my popsicle in your toy chest."
                "Even my boogers are spicy!"
                "That's my swingset, and that's my sandbox. I'm not allowed to go in the deep end."
                "I glued my head to my shoulder, now I have two owies."
                "Me fail English? That's unpossible!"
                "I'm a brick!"
                "I can't see my forehead!"
                "My cat's breath smells like cat food."
        )

        rand_quote="${quotes[ $random % ${#quotes[@]} ]}"
        echo "$rand_quote"
}

msg() {
  message="${1:-null}"
  if [ "$message" == "null" ]; then
        message="$(ralph_quote)"
  fi
  if [[ -z $str ]]; then
        message="$(ralph_quote)"
  fi
  curl -d "${message}" ntfy.sh/${NTFY_TOPIC}
}

alias py=python3
alias python=python3
        '''
        self.runner.write_file_and_execute('.bash_aliases', setup_github_contents)
    
    def aider_install(self):
        
        # Maybe required:
        # python3 -m venv .venv
        # source .venv/bin/activate
        # sudo apt install python3-venv
        
        # On Ubuntu 24, using aider-install simplifies setup and manages Python versions.
        # actual pip package is called 'aider-chat'
        self.runner.run(['pip', 'install', 'aider-install'])
        self.runner.run(['aider-install'])
        
        # This should go into your PROJECT directory
        # TBD finish/fix me.
        aider_conf_contents=""
        self.runner.write_file_and_execute('.aider.conf.yml', aider_conf_contents)
    
    def aider_ralph_install(self):
        
        # run aider-ralph
        # aider-ralph -m 30
    
    
    def run_full_setup(self):
        """Execute the complete setup process."""
        print("\n" + "="*70)
        print("  Ralph-Loop VM Setup Script")
        print("="*70)
        
        try:
            self.setup_ssh_keys()           # ✓
            self.setup_github_cli()         # ✓ Requires gh install
            self.clone_and_configure_git()
            self.setup_nodejs()
            self.setup_api_key()
            self.setup_playwright()
            self.user_bash_files()
            self.aider_install()
            
            
            # Extract repo name from URL
            repo_name = self.github_repo.split('/')[-1].replace('.git', '')
            self.sync_repository(repo_name)
            
            self.h1("Setup Complete!")
            print("Your VM is now configured for Ralph-Loop development.")
            print("\nNext steps:")
            print("  1. Complete GitHub CLI authentication: gh auth login")
            print("  2. Add your SSH key to GitHub (see above)")
            print("  3. Navigate to your repository and start developing!")
            
        except Exception as e:
            print(f"\n❌ Setup failed with error: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point for the setup script."""
    
    # Configuration - IMPORTANT: Do not hardcode sensitive values!
    # These should be passed as environment variables or command-line arguments
    GITHUB_REPO = os.getenv('GITHUB_REPO', '')
    EMAIL = os.getenv('GIT_EMAIL', '{{your-masked-github-email-here@users.noreply.github.com}}')
    API_KEY = os.getenv('OPENROUTER_API_KEY', '{{inject-your-key-here-do-not-hardcode}}')
    PROJECT_REPO = os.getenv('PROJECT_REPO', '{{https://github.com/your-github-user/your-github-repo.git}}')
    
    # Validate configuration
    if '{{' in EMAIL or '{{' in API_KEY:
        print("\n❌ ERROR: Please configure environment variables before running!", file=sys.stderr)
        print("\nRequired environment variables:")
        print("  export GIT_EMAIL='your-email@users.noreply.github.com'")
        print("  export OPENROUTER_API_KEY='your-api-key-here'")
        print("  export PROJECT_REPO='https://github.com/your-username/your-repo.git'")
        sys.exit(1)
    
    # Run setup
    setup = VMSetup(
        github_repo=GITHUB_REPO,
        email=EMAIL,
        api_key=API_KEY,
        project_repo=PROJECT_REPO
    )
    
    setup.run_full_setup()


if __name__ == '__main__':
    main()
