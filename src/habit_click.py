import click 
from rich.console import Console
from rich.table import Table
from user_manager import UserManager
from habit_manager import HabitManager
from db_connection import DBConnection
from exceptions import *
from datetime import datetime
db = DBConnection("../db/habit_tracker.db")

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

    Args:
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

    Args:
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

    Args:
        name (str): The username of the user to delete.
        id (int): The user ID of the user to delete.
    """
    try:
        if id:
            u_manager.delete_user_by_id(id)
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

    Args:
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

    Args:
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

    Args:
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
    """
    try:
        if h_manager.get_habit_from_user_by_id(user_id, habit_id):
            h_manager.update_habit_periodicity(habit_id, new_periodicity)
        click.echo("Habit periodicity updated successfully.")
    except HabitNotFoundException as e:
        click.echo(f"Error: {str(e)}")



def display_habits_table(habits):
    """
    Display habits in a table using Rich library.

    Args:
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


    





if __name__ == "__main__":
    cli()