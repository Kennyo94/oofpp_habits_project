from textual import events, on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import ScrollableContainer, Container, Horizontal, Vertical
from textual.widgets import Button, Header, Input, Label, Static, Footer, ListView, ListItem
from textual.widget import Widget
from db_connection import DBConnection
from habit_manager import HabitManager
from user_manager import UserManager
from exceptions import HabitNotFoundException, HabitAlreadyExistsException

db = DBConnection("../db/habit_tracker.db")
user_manager = UserManager(db)



class UserListView(ListView):

    def __init__(self):
        super().__init__()
        self.users = user_manager.get_users()
    

    def compose(self) -> ComposeResult:
        with ListView():
            for user in self.users:
                yield ListItem(Label(user.get_username()))





class LoginScreen(Widget):
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Button("Create User"), 
            Button("Login User"),
        )

    @on(Button.Pressed)
    def show_users(self):

        pass

class InitialDisplayInfo(Widget):

    text_str = """Welcome to HabitTracker CLI!\nHabitTracker is a versatile tool designed to help you establish and track your daily and weekly habits effectively. Whether you're aiming to cultivate healthy habits, stay organized with daily tasks, or break old patterns, HabitTracker CLI provides the functionality you need to manage your habits seamlessly.
                """
    def compose(self) -> ComposeResult:
        yield Label(self.text_str, classes="displaylabel")






class DisplayMenu(Widget):
    def compose(self) -> ComposeResult:
        yield LoginScreen()
    

class DisplayInfo(Widget):
    def compose(self) -> ComposeResult: 
        yield InitialDisplayInfo()
        
    

class HabitTrackerApp(App):

    CSS_PATH = "style.tcss"

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Vertical(
                DisplayMenu(),
                classes="column",
                ),
            Vertical(
                DisplayInfo(),
                classes="column",
                ),
            )
        yield Input()        
        yield Footer()


app = HabitTrackerApp()

if __name__ == "__main__":
    app.run()