"""
.SYNOPSIS
    Universal Python Package Installer
    Detects and uses available package managers to install dependencies.

.EXAMPLE
    .USAGE
    # Make it executable
    chmod +x install_deps.py

    # Run it
    python install_deps.py
    # or
    ./install_deps.py
"""
#!/usr/bin/env python3


import subprocess
import sys
import os
from pathlib import Path
import shutil


class PackageInstaller:
    """Attempts to install packages using multiple package managers in order of preference."""
    
    TOOL_ORDER = ['uv', 'poetry', 'pdm', 'conda', 'pipenv', 'pip']
    
    def __init__(self):
        self.project_root = Path.cwd()
        
    def is_tool_available(self, tool_name):
        """Check if a tool is available in PATH."""
        return shutil.which(tool_name) is not None
    
    def has_project_file(self, filenames):
        """Check if any of the specified files exist in the project."""
        return any((self.project_root / f).exists() for f in filenames)
    
    def run_command(self, cmd, tool_name):
        """Run a command and return success status."""
        print(f"\n{'='*60}")
        print(f"Attempting to install with: {tool_name}")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'='*60}\n")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            if result.returncode == 0:
                print(f"\n✓ Successfully installed dependencies with {tool_name}")
                return True
            else:
                print(f"\n✗ {tool_name} failed with exit code {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"\n✗ {tool_name} timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"\n✗ {tool_name} failed with error: {e}")
            return False
    
    def try_uv(self):
        """Install with uv."""
        if not self.is_tool_available('uv'):
            return False
        
        # Try uv sync first (for pyproject.toml with uv)
        if self.has_project_file(['pyproject.toml', 'uv.lock']):
            if self.run_command(['uv', 'sync'], 'uv'):
                return True
        
        # Try uv pip install
        if self.has_project_file(['requirements.txt']):
            if self.run_command(['uv', 'pip', 'install', '-r', 'requirements.txt'], 'uv'):
                return True
        
        if self.has_project_file(['pyproject.toml']):
            if self.run_command(['uv', 'pip', 'install', '-e', '.'], 'uv'):
                return True
        
        return False
    
    def try_poetry(self):
        """Install with poetry."""
        if not self.is_tool_available('poetry'):
            return False
        
        if not self.has_project_file(['pyproject.toml', 'poetry.lock']):
            return False
        
        return self.run_command(['poetry', 'install'], 'poetry')
    
    def try_pdm(self):
        """Install with pdm."""
        if not self.is_tool_available('pdm'):
            return False
        
        if not self.has_project_file(['pyproject.toml', 'pdm.lock']):
            return False
        
        return self.run_command(['pdm', 'install'], 'pdm')
    
    def try_conda(self):
        """Install with conda."""
        if not self.is_tool_available('conda'):
            return False
        
        # Try environment.yml first
        if self.has_project_file(['environment.yml', 'environment.yaml']):
            env_file = 'environment.yml' if (self.project_root / 'environment.yml').exists() else 'environment.yaml'
            if self.run_command(['conda', 'env', 'update', '-f', env_file], 'conda'):
                return True
        
        # Try requirements.txt
        if self.has_project_file(['requirements.txt']):
            if self.run_command(['conda', 'install', '--yes', '--file', 'requirements.txt'], 'conda'):
                return True
        
        return False
    
    def try_pipenv(self):
        """Install with pipenv."""
        if not self.is_tool_available('pipenv'):
            return False
        
        if not self.has_project_file(['Pipfile', 'Pipfile.lock']):
            return False
        
        return self.run_command(['pipenv', 'install'], 'pipenv')
    
    def try_pip(self):
        """Install with pip (fallback)."""
        if not self.is_tool_available('pip'):
            # Try pip3
            if self.is_tool_available('pip3'):
                pip_cmd = 'pip3'
            else:
                return False
        else:
            pip_cmd = 'pip'
        
        # Try requirements.txt
        if self.has_project_file(['requirements.txt']):
            if self.run_command([pip_cmd, 'install', '-r', 'requirements.txt'], 'pip'):
                return True
        
        # Try pyproject.toml
        if self.has_project_file(['pyproject.toml']):
            if self.run_command([pip_cmd, 'install', '-e', '.'], 'pip'):
                return True
        
        # Try setup.py
        if self.has_project_file(['setup.py']):
            if self.run_command([pip_cmd, 'install', '-e', '.'], 'pip'):
                return True
        
        return False
    
    def install(self):
        """Main installation method - tries tools in order until one succeeds."""
        print("=" * 60)
        print("Universal Python Package Installer")
        print("=" * 60)
        print(f"Project directory: {self.project_root}")
        print(f"Tool order: {' → '.join(self.TOOL_ORDER)}")
        
        # Detect available tools
        available_tools = [tool for tool in self.TOOL_ORDER if self.is_tool_available(tool)]
        print(f"\nAvailable tools: {', '.join(available_tools) if available_tools else 'None'}")
        
        if not available_tools:
            print("\n✗ No package managers found in PATH!")
            print("Please install at least one: pip, pipenv, poetry, pdm, conda, or uv")
            return False
        
        # Try each tool in order
        tool_methods = {
            'uv': self.try_uv,
            'poetry': self.try_poetry,
            'pdm': self.try_pdm,
            'conda': self.try_conda,
            'pipenv': self.try_pipenv,
            'pip': self.try_pip,
        }
        
        for tool in self.TOOL_ORDER:
            if tool in available_tools:
                try:
                    if tool_methods[tool]():
                        print(f"\n{'='*60}")
                        print(f"✓ Installation completed successfully with {tool}!")
                        print(f"{'='*60}\n")
                        return True
                except Exception as e:
                    print(f"\n✗ Unexpected error with {tool}: {e}")
                    continue
        
        print("\n" + "="*60)
        print("✗ All installation methods failed!")
        print("="*60)
        print("\nPlease check:")
        print("1. You have the correct dependency files in your project")
        print("2. Your dependency files are properly formatted")
        print("3. You have network connectivity")
        print("4. Package names in your dependencies are correct")
        return False


def main():
    installer = PackageInstaller()
    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()