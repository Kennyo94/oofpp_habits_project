import click 
from user_manager import UserManager
from habit_manager import HabitManager
from db_connection import DBConnection
from exceptions import *
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



import click

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





if __name__ == "__main__":
    cli()