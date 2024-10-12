"""
DomainManager.py - A Python-based script to manage Nginx subdomains with SSL certificates.
Version: 1.0.3

Requires: Python 3.6+, PyYAML, colorama
"""

# Main Function
import os
import sys

from colorama import init

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from domain_manager.config import load_config
from domain_manager.logger import setup_logging
from src.domain_manager.updater import check_for_updates
from domain_manager.utils.display import display_startup, main_menu
from domain_manager.utils.permissions import check_permissions
from domain_manager._version import __version__

# Initialize colorama
init(autoreset=True)

# Example usage
package_name = "NGINXDomainManager"


def main():
    # Ensure the script is run as root/admin
    check_permissions()

    # Load configuration
    config = load_config()

    # Setup logging
    setup_logging(config['log_file'])

    # Display startup graphic
    display_startup(__version__)

    # Check for updates
    check_for_updates(__version__, package_name)

    # Proceed with the main menu
    main_menu(config)


if __name__ == "__main__":
    main()
