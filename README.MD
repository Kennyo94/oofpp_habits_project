# Habit Tracking App

Welcome to HabitTracker, a simple command-line interface (CLI) application designed to help you track and analyze your habits effectively. Whether you're aiming to exercise more regularly, stay organized, or practice mindfulness, HabitTracker provides you with the tools you need to stay accountable and achieve your goals.

## Installation

To install HabitTracker, follow these steps:

1. Clone the repository to your local machine:

```git clone https://github.com/Kennyo94/habit-tracking-app.git```


2. Navigate to the project directory:

```cd habit-tracker```


3. Create and activate a virtual environment using venv (optional but recommended):

On Unix or MacOS:

```python3 -m venv venv```
```source venv/bin/activate```

On Windows:

```python -m venv venv```
```.\venv\Scripts\activate```

4. Install the required Python packages using pip:

```pip install -r requirements.txt```

5. Run Unit Tests 

```cd tests```
```pytest```

## Functionalities

HabitTracker offers the following functionalities:

- **Create User**: Create a new user in the system.
- **Select User**: Select an existing user to perform actions.
- **Delete User**: Delete an existing user from the system.
- **Create Habit**: Create a new habit and associate it with a user.
- **Get Habits**: Get the habits of a user.
- **Complete Habit**: Mark a habit as completed.
- **Update Habit Name**: Update the name of a habit.
- **Update Habit Periodicity**: Update the periodicity of a habit.
- **View Habit**: View detailed information about a habit.
- **Analytics**: Retrieve analytics data, including:
    - List of all currently tracked habits.
    - List of habits with the same periodicity.
    - Longest run streak of all defined habits.
    - Longest run streak for a given habit.

## Usage

To use HabitTracker, follow these steps:

1. Navigate to the project directory in your terminal.

2. Run the CLI application by executing the following command:

```python main.py```

3. Follow the prompts and commands provided by the CLI to create users, manage habits, view analytics, and more. To see all possible commands type:

```python main.py --help```


