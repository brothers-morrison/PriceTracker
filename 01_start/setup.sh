

#ssh-keygen -t rsa -b 4096 -C "14063813+brothers-morrison@users.noreply.github.com"

function install_python_tools()
{
	sudo apt update
	sudo apt install python3 python3-venv

	env_name=".venv"
	python3 -m venv $env_name
	source $env_name/bin/activate

	# Python 3.12 or higher
	python3 --version
	pip --version
	
	pip install pytest
}
install_python_tools

# Set environment variables (never hardcode sensitive data!)
export GIT_EMAIL='14063813+brothers-morrison@users.noreply.github.com'
export OPENROUTER_API_KEY='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'
export GITHUB_REPO='git@github.com:brothers-morrison/PriceTracker.git'  # optional

# Dont do this here, instead prefer the .aider.conf.yml file ?
# automatically commit to GIT
export AIDER_DARK_MODE=True

# Run the script
chmod +x vm_setup_script.py
python3 vm_setup_script.py