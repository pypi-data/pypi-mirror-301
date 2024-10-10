import argparse
import os
import time

from rich.console import Console
from rich.text import Text

from swarms_cloud.cli.onboarding import OnboardingProcess

console = Console()


ASCII_ART = """
  _________                                     
 /   _____/_  _  _______ _______  _____   ______
 \_____  \\ \/ \/ /\__  \\_  __ \/     \ /  ___/
 /        \\     /  / __ \|  | \/  Y Y  \\___ \ 
/_______  / \/\_/  (____  /__|  |__|_|  /____  >
        \/              \/            \/     \/ 

"""

# Function to display the ASCII art in red
def show_ascii_art():
    text = Text(ASCII_ART, style="bold red")
    console.print(text)


# Help command
def show_help():
    console.print(
        """
    [bold cyan]Swarms Cloud CLI - Help[/bold cyan]

    [bold magenta]Commands:[/bold magenta]
    [bold white]onboarding[/bold white]    : Starts the onboarding process
    [bold white]help[/bold white]          : Shows this help message
    [bold white]get-api-key[/bold white]   : Retrieves your API key from the platform
    [bold white]check-login[/bold white]   : Checks if you're logged in and starts the cache

    For more details, visit: https://docs.swarms.world
    """
    )


# Fetch API key from platform
def get_api_key():
    console.print("[bold yellow]Fetching your API key...[/bold yellow]")
    # Simulating API key retrieval process
    time.sleep(2)
    console.print("[bold green]Your API key is: XXXXXXXXXXXXX[/bold green]")
    # In reality, you'd fetch this from https://swarms.world/platform/api-keys


# Check and start cache (login system simulation)
def check_login():
    cache_file = "cache.txt"

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache_content = f.read()
        if cache_content == "logged_in":
            console.print("[bold green]You are already logged in.[/bold green]")
        else:
            console.print("[bold red]You are not logged in.[/bold red]")
    else:
        console.print("[bold yellow]Logging in...[/bold yellow]")
        time.sleep(2)
        with open(cache_file, "w") as f:
            f.write("logged_in")
        console.print("[bold green]Login successful![/bold green]")


# Main CLI handler
def main():
    parser = argparse.ArgumentParser(description="Swarms Cloud CLI")

    # Adding arguments for different commands
    parser.add_argument(
        "command",
        choices=["onboarding", "help", "get-api-key", "check-login"],
        help="Command to run",
    )

    args = parser.parse_args()
    
    show_ascii_art()

    # Determine which command to run
    if args.command == "onboarding":
        OnboardingProcess().run()
    elif args.command == "help":
        show_help()
    elif args.command == "get-api-key":
        get_api_key()
    elif args.command == "check-login":
        check_login()
    else:
        console.print("[bold red]Unknown command! Type 'help' for usage.[/bold red]")


if __name__ == "__main__":
    main()
