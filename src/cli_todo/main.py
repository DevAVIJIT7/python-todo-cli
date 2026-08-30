import typer
from cli_todo.database import TodoDatabase
from cli_todo.model import Todo

db = TodoDatabase()
app = typer.Typer(help="A lightning-fast Python CLI To-Do App.")

@app.command()
def add(task: str):
    """
    Add a new task to the to-do list.
    """
    # Logic to add the task goes here
    todo = Todo(title=task, task_id=str(db.get_next_id()))
    db.save_single_task(todo)
    typer.echo(f"Task added: {todo.title} (ID: {todo.task_id})")

@app.command()
def list():
    """
    List all tasks in the to-do list.
    """
    # Logic to list tasks goes here
    todos = db.get_all_tasks()
    for todo in todos:
        typer.echo(f"- {todo.title} (ID: {todo.task_id})")

@app.command()
def update(task_id: int, new_task: str, completed: bool = False):
    """
    Update an existing task in the to-do list.
    """
    # Logic to update the task goes here
    todo = db.get_task_by_id(task_id)
    if todo:
        todo.update(title=new_task, completed=completed)
        db.save_single_task(todo)
        typer.echo(f"Task {task_id} updated to: {new_task}")
    else:
        typer.echo(f"Task {task_id} not found.")

@app.command()
def delete(task_id: int):
    """
    Delete a task from the to-do list.
    """
    # Logic to delete the task goes here
    if db.delete_task_by_id(task_id):
        typer.echo(f"Task {task_id} deleted.")
    else:
        typer.echo(f"Task {task_id} not found.")