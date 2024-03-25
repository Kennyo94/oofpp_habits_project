import click 
from rich.console import Console
from rich.table import Table
from src.user_manager import UserManager
from src.habit_manager import HabitManager
from src.db_connection import DBConnection
from src.exceptions import *
from src.analytics import get_all_tracked_habits, get_habits_by_periodicity, get_longest_run_streak_all_habits, get_longest_run_streak_for_habit 
from datetime import datetime

# Create a DB connection
db = DBConnection("db/habit_tracker.db")

# Initialize user and habit managers
u_manager = UserManager(db)
h_manager = HabitManager(db)


@click.group()
def cli():
    """Welcome to HabitTracker CLI"""
    pass

@cli.command()
@click.argument('username')
def create_user(username):
    """
    Create a new user in the HabitTracker system.

    Paramters:
        username (str): The username of the new user to be created.
    """
    try:
        result = u_manager.create_user(username)
        click.echo(result)
    except UsernameAlreadyExistsException as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@click.option('--name', '-n', help='Select user by name.')
@click.option('--id', '-i', type=int, help='Select user by ID.')
def select_user(name, id):
    """
    Select an existing user in the HabitTracker system.

    Paramters:
        name (str): The username of the user to select.
        id (int): The user ID of the user to select.
    """
    try:
        if id:
            user = u_manager.get_user_by_id(id)
        elif name:
            user = u_manager.get_user_by_name(name)
        else:
            raise click.BadParameter("Please provide either --name or --id option.")
        
        click.echo(user)
    except (UserNotFoundException, ValueError) as e:
        click.echo(f"Error: {str(e)}")




@cli.command()
@click.option('--name', '-n', help='Delete user by username.')
@click.option('--id', '-i', type=int, help='Delete user by ID.')
@click.confirmation_option(prompt='Are you sure you want to delete this user?')
def delete_user(name, id):
    """
    Delete an existing user from the HabitTracker system.

    Paramters:
        name (str): The username of the user to delete.
        id (int): The user ID of the user to delete.
    """
    try:
        if id:
            username = input("Confirm username: ")
            if u_manager.get_user_by_name(username).get_user_id() == id:
                u_manager.delete_user_by_id(id)
            else:
                click.echo("Error: User ID and Username does not match")
                return 
        elif name:
            u_manager.delete_user_by_username(name)
        else:
            raise click.BadParameter("Please provide either --name or --id option.")
        click.echo("User deleted successfully.")
    except (UserNotFoundException, ValueError) as e:
        click.echo(f"Error: {str(e)}")
    


@cli.command()
@click.option('--name', '-n',type=str, prompt='Enter habit name', help='Name of the habit.')
@click.option('--periodicity', '-p', type=click.Choice(['daily', 'weekly']), prompt='Enter habit periodicity', help='Periodicity of the habit.')
@click.option('--user_id', '-u', prompt='Enter user ID', help='User ID associated with the habit.')
def create_habit(name, periodicity, user_id):
    """
    Create a new habit and associate it with a user.

    Paramters:
        name (str): The name of the habit.
        periodicity (str): The periodicity of the habit (daily or weekly).
        user_id (int): The user ID associated with the habit.
    """
    try:
        id = int(user_id)
        h_manager.add_habit_by_info(name, periodicity, id)
        click.echo("Habit created successfully.")
    except (UserNotFoundException, HabitAlreadyExistsException, InvalidPeriodicityException) as e:
        click.echo(f"Error: {str(e)}")



@cli.command()
@click.option('--user_id', '-i', type=int, help='User ID to get habits.')
def get_habits(user_id):
    """
    Get the habits of a user by user ID.

    Paramters:
        user_id (int): The ID of the user.
    """
    try:
        if user_id:
            habits = h_manager.get_habits_from_user(user_id)
        else:
            raise click.BadParameter("User ID must be provided.")

        if habits:
            display_habits_table(habits)
        else:
            click.echo("No habits found for the specified user.")

    except UserNotFoundException as e:
        click.echo(f"Error: {str(e)}")



@cli.command()
@click.option('--user_id', type=int, help='ID of the user completing the habit.')
@click.option('--habit_id', type=int, help='ID of the habit to complete.')
@click.option('--habit_name', help='Name of the habit to complete.')
def complete_habit(user_id, habit_id, habit_name):
    """
    Complete a habit by its ID or name.

    Paramters:
        user_id (int): ID of the user completing the habit.
        habit_id (int): ID of the habit to complete.
        habit_name (str): Name of the habit to complete.
    """
    try:
        if not user_id:
            raise click.BadParameter("User ID must be provided.")
        if not habit_id and not habit_name:
            display_habits_table(h_manager.get_habits_from_user(user_id))
            habit_choice = int(input("Please Select Habit by ID: "))
            h_manager.complete_habit(habit_choice, datetime.now())
            click.echo("Habit completed successfully.")
        if habit_id:
            h_manager.complete_habit(habit_id, datetime.now())
            click.echo("Habit completed successfully.")
        elif habit_name:
            new_habit_id = h_manager.get_habit_by_name(habit_name).get_habit_id()
            h_manager.complete_habit(new_habit_id, datetime.now())
            click.echo("Habit completed successfully.")

    except HabitNotFoundException as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@click.option('--user_id', type=int, help='The ID of the user who owns the habit.')
@click.option('--habit_id', type=int, help='The ID of the habit to update.')
@click.option('--new_name', type=str, help='The new name for the habit.')
def update_habit_name(user_id, habit_id, new_name):
    """
    Update the name of a habit.

    Paramters:
        user_id (int): The ID of the user who owns the habit.
        habit_id (int): The ID of the habit to update.
        new_name (str): The new name for the habit.
    """
    try:
        if h_manager.get_habit_from_user_by_id(user_id, habit_id):
            h_manager.update_habit_name(habit_id, new_name)
            click.echo("Habit name updated successfully.")
    except HabitNotFoundException as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option('--user_id', type=int, help='The ID of the user who owns the habit.')
@click.option('--habit_id', type=int, help='The ID of the habit to update.')
@click.option('--new_periodicity', type=str, help='The new periodicity for the habit.')
def update_habit_periodicity(user_id, habit_id, new_periodicity):
    """
    Update the periodicity of a habit.

    Paramters:
        user_id (int): The ID of the user who owns the habit.
        habit_id (int): The ID of the habit to update.
        new_periodicity (str): The new periodicity for the habit.
    """
    try:
        if h_manager.get_habit_from_user_by_id(user_id, habit_id):
            h_manager.update_habit_periodicity(habit_id, new_periodicity)
        click.echo("Habit periodicity updated successfully.")
    except HabitNotFoundException as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option('--user_id', type=int, help='The ID of the user who owns the habit.')
@click.option('--habit_id', type=int, help='The ID of the habit to view.')
def view_habit(user_id, habit_id):
    """
    View detailed habit information.

    Paramters:
        user_id (int): The ID of the user who owns the habit.
        habit_id (int): The ID of the habit to view.
    """
    try: 
        habit = h_manager.get_habit_from_user_by_id(user_id, habit_id)
        display_habit(habit)
    except HabitNotFoundException as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
@click.option('--habit_id','-id', type=int, prompt='Enter habit ID', help='ID of the habit to delete.')
@click.confirmation_option(prompt='Are you sure you want to delete this habit?')
def delete_habit(habit_id):
    """
    Delete a habit by its ID.

    Paramters:
        habit_id (int): The ID of the habit to delete.
    """
    try:
        h_manager.delete_habit(habit_id)
        click.echo("Habit deleted successfully.")
    except HabitNotFoundException as e:
        click.echo(f"Error: {str(e)}")


@cli.command()
def analytics_get_habits():
    """
    Return a list of all currently tracked habits.

    This command retrieves all currently tracked habits from the Habit Manager
    and displays them in a table.
    """
    habits = get_all_tracked_habits(h_manager)
    display_habits_table(habits)

@cli.command()
@click.option('--periodicity','-p', type=str, help='Filter habits by periodicity')
def analytics_habits_periodicity(periodicity):
    """
    Return a list of all habits with the same periodicity.

    Args:
        periodicity (str): The periodicity to filter habits by.

    This command retrieves habits with the specified periodicity from the Habit Manager
    and displays them in a table.
    """
    habits = get_habits_by_periodicity(h_manager, periodicity)
    display_habits_table(habits)


@cli.command()
def analytics_longest_streak():
    """
    Return the longest run streak of all defined habits.

    This command calculates the longest run streak among all defined habits
    and displays the habit with its corresponding streak dates in a table.
    """
    habits = h_manager.get_habits()
    streak = get_longest_run_streak_all_habits(habits)
    display_habit_table(streak[0])
    click.echo(f"Longest Streak Dates: {streak[1]}")


@cli.command()
@click.option('--habit_id','-id', type=str, help='Filter habits by periodicity')
def analytics_habit_longest_streak(habit_id):
    """
    Return the longest run streak for a given habit.

    Args:
        habit_id (str): The ID of the habit to retrieve the longest streak for.

    This command calculates the longest run streak for the specified habit
    and displays it.
    """
    habit = h_manager.get_habit_by_id(habit_id)
    streak = get_longest_run_streak_for_habit(habit)
    click.echo(f"Longest Streak: {streak}")




def display_habits_table(habits):
    """
    Display habits in a table using Rich library.

    Paramters:
        habits (list): List of Habit objects.
    """
    console = Console()

    table = Table(title="User Habits")
    table.add_column("Habit ID", style="white", justify="left")
    table.add_column("Habit Name", style="cyan", justify="left")
    table.add_column("Periodicity", style="magenta", justify="center")
    table.add_column("Current Streak", style="yellow", justify="center")
    table.add_column("Longest Streak", style="green", justify="center")

    for habit in habits:
        table.add_row(
            str(habit.get_habit_id()),
            habit.get_name(),
            habit.get_periodicity(),
            str(habit.get_current_streak()),
            str(habit.get_longest_streak())
        )

    console.print(table)


def display_habit_table(habit):
    """
    Display information about a single habit without completion dates.

    Paramters:
        habit (Habit): The Habit object to display information about.
    """    
    console = Console()

    # Create a table for habit information
    habit_table = Table(title="Habit Information", style="bold blue")
    habit_table.add_column("Attribute", style="bold")
    habit_table.add_column("Value", style="bold")
    habit_table.add_row("Habit ID", str(habit.get_habit_id()))
    habit_table.add_row("Name", habit.get_name())
    habit_table.add_row("Periodicity", habit.get_periodicity())
    habit_table.add_row("Creation Date", habit.get_creation_date())
    habit_table.add_row("Current Streak", str(habit.get_current_streak()), style="green")
    habit_table.add_row("Longest Streak", str(habit.get_longest_streak()), style="green")

    # Print the tables
    console.print(habit_table)

def display_habit(habit):
    """
    Display information about a single habit.

    Paramters:
        habit (Habit): The Habit object to display information about.
    """    
    console = Console()

    # Create a table for habit information
    habit_table = Table(title="Habit Information", style="bold blue")
    habit_table.add_column("Attribute", style="bold")
    habit_table.add_column("Value", style="bold")
    habit_table.add_row("Habit ID", str(habit.get_habit_id()))
    habit_table.add_row("Name", habit.get_name())
    habit_table.add_row("Periodicity", habit.get_periodicity())
    habit_table.add_row("Creation Date", habit.get_creation_date())
    habit_table.add_row("Current Streak", str(habit.get_current_streak()), style="green")
    habit_table.add_row("Longest Streak", str(habit.get_longest_streak()), style="green")

    # Create a table for last 5 completion dates
    completion_table = Table(title="Last 5 Completion Dates", style="bold blue")
    completion_table.add_column("Date", style="bold")
    for date in habit.get_completion_history()[-5:]:
        completion_table.add_row(str(date))

    # Print the tables
    console.print(habit_table)
    console.print(completion_table)




