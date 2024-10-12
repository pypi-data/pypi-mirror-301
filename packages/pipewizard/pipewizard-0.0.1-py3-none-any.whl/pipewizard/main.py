from rich import print
import questionary

def validate_not_empty(response, prompt):
    """Validate that the response is not empty. Repeat the question if it is."""
    while not response:
        print(f"[bold red]You must choose at least one option for {prompt}.[/bold red]")
        response = questionary.checkbox(
            prompt, choices=["Test", "Lint", "Docker"]
        ).ask()
    return response


def validate_text_not_empty(response, prompt):
    """Validate that the text is not empty. Repeat the question if it is."""
    while not response:
        print(f"[bold red]You must provide a value for {prompt}.[/bold red]")
        response = questionary.text(prompt).ask()
    return response

print("[bold green]Welcome to Pipewizard![/bold green]")


name = validate_text_not_empty(questionary.text("What's the name of the project?").ask(), "What's the name of the project?")

print(f"The name for the project is [bold blue]{name}[/bold blue]")


jobs = validate_not_empty(questionary.checkbox(
    "Select jobs", choices=["Test", "Lint", "Docker"]
).ask(), "Select jobs")

print(f"Selected jobs: {jobs}")


version = questionary.select(
    "Select Python version", choices=["3.10", "3.11", "3.12"], default="3.12"
).ask()

print(f"Selected Python version: {version}")