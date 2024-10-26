from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setting up the database
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Define the Task table
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    deadline = Column(Date, nullable=False)


Base.metadata.create_all(engine)


def show_missed_tasks(db_session):
    today = datetime.today().date()
    missed_tasks = db_session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()

    if not missed_tasks:
        print("All tasks have been completed!")
    else:
        print("Missed tasks:")
        for i, task in enumerate(missed_tasks, 1):
            print(f"{i}. {task.task}. {task.deadline.strftime('%d %b')}")


def delete_task(db_session):
    tasks = db_session.query(Task).order_by(Task.deadline).all()

    if not tasks:
        print("Nothing to delete!")
        return

    print("Choose the number of the task you want to delete:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.task}. {task.deadline.strftime('%d %b')}")

    task_number = int(input("> ")) - 1
    if 0 <= task_number < len(tasks):
        db_session.delete(tasks[task_number])
        db_session.commit()
        print("The task has been deleted!")
    else:
        print("Invalid task number.")


# Function to add a task
def add_task():
    task_name = input("Enter a task \n> ")
    deadline_str = input("Enter a deadline (YYYY-MM-DD) \n> ")
    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
    task = Task(task=task_name, deadline=deadline)
    session.add(task)
    session.commit()
    print("The task has been added!")


# Function to print today's tasks
def today_tasks():
    today = datetime.today().date()
    tasks = session.query(Task).filter(Task.deadline == today).all()
    print(f"Today {today.strftime('%d %b')}:")
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        for task in tasks:
            print(f"{task.id}. {task.task}")


# Function to print the week's tasks
def week_tasks():
    today = datetime.today()
    for i in range(7):
        day = today + timedelta(days=i)
        tasks = session.query(Task).filter(Task.deadline == day.date()).all()
        print(f"{day.strftime('%A %d %b')}:")
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            for task in tasks:
                print(f"{task.id}. {task.task}")
        print()


# Function to print all tasks sorted by deadline
def all_tasks():
    tasks = session.query(Task).order_by(Task.deadline).all()
    print("All tasks:")
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        for task in tasks:
            day = task.deadline.day
            month = task.deadline.strftime('%b')
            print(f"{task.id}. {task.task}. {day} {month}")
            #print(f"{task.id}. {task.task}. {task.deadline.strftime('%d %b')}")


# Function to display the menu and execute selected operation
def menu():
    while True:
        print()
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add a task")
        print("6) Delete a task")
        print("0) Exit")
        choice = input()
        print()

        if choice == '1':
            today_tasks()
        elif choice == '2':
            week_tasks()
        elif choice == '3':
            all_tasks()
        elif choice == '4':
            show_missed_tasks(session)
        elif choice == '5':
            add_task()
        elif choice == '6':
            delete_task(session)
        elif choice == '0':
            print("Bye!")
            break
        else:
            print("Invalid option, please choose again.")


if __name__ == "__main__":
    menu()
