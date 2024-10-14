# Display Startup Graphic
import logging
import os

from colorama import Fore, init, Style
from domain_manager._version import __version__
from domain_manager.config import configure_settings, create_nginx_config
from domain_manager.logger import show_logs, show_changelog, setup_logging
from domain_manager.updater import check_for_updates
from domain_manager.utils.domain import list_subdomains, get_subdomain_details, delete_subdomain, \
    obtain_certificate, reload_nginx
from domain_manager.utils.validation import validate_subdomain, validate_ip, validate_port
from click import echo, clear

# Initialize colorama
init(autoreset=True)

package_name = "NGINXDomainManager"

MAIN_MENU_CHOICES = {
    '1': "Create a new subdomain",
    '2': "Edit an existing subdomain",
    '3': "Update existing domains",
    '4': "Delete a subdomain",
    '5': "Settings",
    '6': "Exit"
}

SETTINGS_MENU_CHOICES = {
    '1': "View logs",
    '2': "View Changelog",
    '3': "Configure settings",
    '4': "Check for updates",
    '5': "Go back to the main menu"
}


# Display Startup Graphic and Version
def display_startup(version):
    startup_graphic = f"""
######################################################################################
#   _____                        _         __  __                                    #
#  |  __ \\                      (_)       |  \\/  |                                   #
#  | |  | | ___  _ __ ___   __ _ _ _ __   | \\  / | __ _ _ __   __ _  __ _  ___ _ __  #
#  | |  | |/ _ \\| '_ ` _ \\ / _` | | '_ \\  | |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__| #
#  | |__| | (_) | | | | | | (_| | | | | | | |  | | (_| | | | | (_| | (_| |  __/ |    #
#  |_____/ \\___/|_| |_| |_|\\__,_|_|_| |_| |_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|    #
#                                                                    __/ |           #
#                                                                   |___/            #
######################################################################################
    """
    print(Fore.CYAN + startup_graphic)
    print(f"Version: {version}\n")


# Main Menu
def main_menu(config):
    logger = setup_logging(config['log_file'])
    while True:
        print(f"{Fore.BLUE}\nWhat would you like to do?{Style.RESET_ALL}")
        for key, value in MAIN_MENU_CHOICES.items():
            print(f"{Fore.YELLOW}{key}) {value}{Style.RESET_ALL}")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            handle_create_subdomain(config, logger)
        elif choice == '2':
            handle_edit_subdomain(config, logger)
        elif choice == '3':
            handle_update_domains(config, logger)
        elif choice == '4':
            handle_delete_subdomain(config, logger)
        elif choice == '5':
            settings_menu(config, logger)
        else:
            print(Fore.RED + "Invalid option. Please enter a number between 1 and 6." + Style.RESET_ALL)
            logger.warning(f"User entered invalid main menu choice: {choice}")

        # Wait for user to press Enter before returning to the menu
        input(Fore.MAGENTA + "Press Enter to return to the main menu..." + Style.RESET_ALL)
        clear()
        display_startup(__version__)


def settings_menu(config, logger):
    # Display the settings sub-menu and handle user input
    while True:
        print(f"{Fore.BLUE}\nSettings Menu:{Style.RESET_ALL}")
        for key, value in SETTINGS_MENU_CHOICES.items():
            print(f"{Fore.YELLOW}{key}) {value}{Style.RESET_ALL}")

        sub_choice = input("Enter your choice (1-5): ").strip()

        if sub_choice == '1':
            # View logs
            show_logs(config, logger)  # Pass the logger
        elif sub_choice == '2':
            # View changelog
            show_changelog(logger)  # Pass the logger
        elif sub_choice == '3':
            # Configure settings
            configure_settings(config)
            logger.info("Settings configured by user.")
        elif sub_choice == '4':
            # Check for updates
            check_for_updates(__version__, package_name)
            logger.info("Checked for updates.")
            break
        elif sub_choice == '5':
            # Go back to the main menu
            print(Fore.GREEN + "Returning to the main menu..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid option. Please enter a number between 1 and 5." + Style.RESET_ALL)
            logger.warning(f"User entered invalid settings menu choice: {sub_choice}")
            continue

    # Wait for user to press Enter before returning to the settings menu
    input(Fore.MAGENTA + "Press Enter to continue in Settings..." + Style.RESET_ALL)
    clear()

        if choice == '1':
            # Create a new subdomain
            subdomain = input("Enter your subdomain (e.g., app.example.com): ").strip()
            target_ip = input("Enter the internal IP address of the target server (e.g., 192.168.0.215): ").strip()
            target_port = input("Enter the port the target service is running on (e.g., 8080): ").strip()

            if not validate_subdomain(subdomain) or not validate_ip(target_ip) or not validate_port(target_port):
                continue

            create_nginx_config(config, subdomain, target_ip, target_port)
            obtain_certificate(subdomain)
            reload_nginx()

            print(Fore.GREEN + f"Nginx configuration and SSL setup for {subdomain} complete!")
            logging.info(f"Nginx configuration and SSL setup for {subdomain} complete!")

        elif choice == '2':
            # Edit an existing subdomain
            subdomains = list_subdomains(config)
            if not subdomains:
                continue
            selection = input("Select the number of the subdomain you want to edit (or 'q' to go back): ").strip()
            if selection.lower() == 'q':
                print(Fore.YELLOW + "Deletion cancelled.")
                continue
            details = get_subdomain_details(config, selection)
            if not details:
                print(Fore.RED + "Invalid selection. Please check the number and try again.")
                continue
            subdomain, current_ip, current_port = details
            print(f"Editing subdomain: {subdomain} (Current IP: {current_ip}, Current Port: {current_port})")
            new_ip = input(f"Enter the new internal IP address for {subdomain} [{current_ip}]: ").strip() or current_ip
            new_port = input(f"Enter the new port for {subdomain} [{current_port}]: ").strip() or current_port

            if not validate_ip(new_ip) or not validate_port(new_port):
                continue

            create_nginx_config(config, subdomain, new_ip, new_port)
            obtain_certificate(subdomain)
            reload_nginx()

            print(Fore.GREEN + f"Nginx configuration and SSL setup for {subdomain} updated!")
            logging.info(f"Nginx configuration and SSL setup for {subdomain} updated!")

        elif choice == '3':
            # Update existing domains
            print("Updating SSL certificates for all existing domains...")
            subdomains = list_subdomains(config)
            if not subdomains:
                continue
            for sub in subdomains:
                print(f"Updating SSL certificate for {sub}...")
                obtain_certificate(sub)
            reload_nginx()
            print(Fore.GREEN + "All domains updated.")
            logging.info("All domains updated.")

        elif choice == '4':
            # Delete a subdomain
            subdomains = list_subdomains(config)
            if not subdomains:
                continue
            selection = input("Select the number of the subdomain you want to delete (or 'q' to go back): ").strip()
            if selection.lower() == 'q':
                print(Fore.YELLOW + "Deletion cancelled.")
                continue
            details = get_subdomain_details(config, selection)
            if not details:
                print(Fore.RED + "Invalid selection. Please check the number and try again.")
                continue
            subdomain = details[0]
            confirmation = input(
                f"Are you sure you want to delete the subdomain {subdomain}? This action cannot be undone. (yes/no): ").strip().lower()
            if confirmation != 'yes':
                print(Fore.YELLOW + "Deletion cancelled.")
                continue
            delete_subdomain(config, subdomain)

        elif choice == '5':
            while True:
                print("\nWhat would you like to do?")
                print("1) View logs")
                print("2) View Changelog")
                print("3) Configure settings")
                print("4) Check for updates")
                print("5) Go back to the main menu")

                sub_choice = input("Enter your choice (1-5): ").strip()



        elif choice == '6':
            # Exit
            print("Goodbye!")
            break

        else:
            print(Fore.RED + "Invalid option. Try again.")
            continue

        # Wait for user to press Enter before returning to the menu
        input("Press Enter to return to the main menu...")
        clear_terminal()
        display_startup(__version__)
