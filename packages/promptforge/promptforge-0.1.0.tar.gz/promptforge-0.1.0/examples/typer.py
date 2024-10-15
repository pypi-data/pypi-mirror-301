import typer
from rich.console import Console

from promptforge.pipeline import prompt_pipeline
from promptforge.utils.cancel import cancel
from promptforge.utils.validators import (
    DateValidator,
    EmailValidator,
    NonEmptyValidator,
)

app = typer.Typer()
console = Console(stderr=True, markup=True)


@app.command()
def register():
    """
    Main function to run the interactive CLI application.
    """
    console.print(
        "\n[bold]Welcome to the User Registration and Survey Application![/bold]\n"
    )

    prompt_definitions = [
        {
            "name": "username",
            "type": "text_input",
            "message": "Enter your username:",
            "validate": NonEmptyValidator(),
        },
        {
            "name": "email",
            "type": "text_input",
            "message": "Enter your email address:",
            "validate": EmailValidator(),
        },
        {
            "name": "accept_terms",
            "type": "confirm",
            "message": "Do you accept the terms and conditions?",
            "default": False,
        },
        {
            "name": "location",
            "type": "cascading_select",
            "message1": "Select your country:",
            "choices1": ["USA", "Canada", "Mexico"],
            "message2": "Select your city:",
            "choices2_dict": {
                "USA": ["New York", "Los Angeles", "Chicago"],
                "Canada": ["Toronto", "Vancouver", "Montreal"],
                "Mexico": ["Mexico City", "Guadalajara", "Monterrey"],
            },
            "default1": "USA",
            "default2": "New York",
        },
        {
            "name": "interests",
            "type": "multiselect",
            "message": "Select your interests:",
            "choices": [
                "Technology",
                "Sports",
                "Music",
                "Art",
                "Science",
                "Travel",
                "Food",
                "Movies",
            ],
            "min_selection": 1,
            "max_selection": 5,
        },
        {
            "name": "communication_method",
            "type": "select",
            "message": "Select your preferred communication method:",
            "choices": ["Email", "Phone", "SMS", "Postal Mail"],
        },
        {
            "name": "event_date",
            "type": "text_input",
            "message": "Enter the event date (YYYY-MM-DD):",
            "default": "2023-01-01",
            "validate": DateValidator(),
        },
    ]

    try:
        prompt_results = prompt_pipeline(
            prompt_definitions,
            on_cancel=lambda results: cancel("Operation cancelled by user."),
        )
    except Exception as e:
        cancel(f"An error occurred: {e}")
        console.print_exception(show_locals=True)
        raise typer.Exit(code=1)

    if not prompt_results.get("accept_terms", False):
        cancel("You must accept the terms and conditions to proceed.")
        raise typer.Exit(code=1)

    username = prompt_results["username"]
    email = prompt_results["email"]
    country, city = prompt_results["location"]
    interests = prompt_results["interests"]
    communication_method = prompt_results["communication_method"]
    event_date = prompt_results["event_date"]
    # Simulate processing with spinner
    console.print("\n[bold green]Registering your information...[/bold green]")

    # Display summary
    console.print("\n[bold]Registration Complete![/bold]")
    console.print(f"Username: {username}")
    console.print(f"Email: {email}")
    console.print(f"Location: {city}, {country}")
    console.print(f"Interests: {', '.join(interests)}")
    console.print(f"Preferred Communication Method: {communication_method}\n")
    console.print(f"Event Date: {event_date}\n")


if __name__ == "__main__":
    app()
