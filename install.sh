#!/bin/bash

echo "give me a bottle of rum!"
#!/bin/bash

# Colors for styling
G="\033[92m"
R="\033[91m"
Y="\033[93m"
RESET="\033[0m"

echo -e "${G}[+] Installing ZAIN-VAULT Locker...${RESET}"

# Check and install python3 & pip if missing
if ! command -v python3 &> /dev/null; then
	echo -e "${Y}[*] Python3 not found. Installing...${RESET}"
	pkg update && pkg install python3 -y || sudo apt update && sudo apt install python3 python3-pip -y
	fi
	
	# Install required cryptography library
	echo -e "${Y}[*] Installing required Python libraries...${RESET}"
	pip3 install cryptography
	
	# Make vault.py executable
	chmod +x vault.py
	
	# Create a global shortcut command 'zain-vault'
	if [ -d "$PREFIX/bin" ]; then
		# For Termux
		CP_PATH="$PREFIX/bin/zain-vault"
		elif [ -d "/usr/local/bin" ]; then
		# For Linux / Parrot OS
		CP_PATH="/usr/local/bin/zain-vault"
		else
			CP_PATH="$HOME/.local/bin/zain-vault"
			mkdir -p "$HOME/.local/bin"
			fi
			
			# Copy script to global path
			if sudo cp vault.py "$CP_PATH" 2>/dev/null || cp vault.py "$CP_PATH" 2>/dev/null; then
				echo -e "${G}[+] Installation Successful!${RESET}"
				echo -e "${Y}[+] You can now run your tool anywhere in the terminal by typing:${RESET} ${G}zain-vault${RESET}"
				else
					echo -e "${R}[-] Installation failed due to permission issues. Try running with sudo.${RESET}"
					fi
