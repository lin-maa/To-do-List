
m sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

today = datetime.today()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Todo:
    rows = list()

    def __init__(self):
        self.today = datetime.today()
        self.mon = today.strftime('%b')
        self.day_of_week = today.strftime('%A')
        self.day_of_month = today.strftime('%d')
        self.user_choice = 1
        self.week = 0

    def __str__(self):
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

    def user_action(self):
        while True:
            self.__str__()
            self.user_choice = int(input())
            if self.user_choice == 0:
                print('Bye!')
                break
            else:
                if self.user_choice in [1, 2, 3, 4, 6]:
                    self.task_type(self.user_choice)
                if self.user_choice == 5:
                    self.add()

    def task_type(self, user_choice):
        self.rows = list()
        if user_choice == 2:  # Week's tasks
            for day_time in range(7):
                self.week = self.today.date() + timedelta(days=day_time)
                self.day_of_week = self.week.strftime('%A')
                self.day_of_month = self.week.strftime('%d')
                self.rows = session.query(Task). \
                    filter(Task.deadline == self.week). \
                    order_by(Task.deadline).all()
                print(f'{self.day_of_week} {self.day_of_month} {self.mon}:')
                self.single_task()
        else:
            if user_choice == 1:  # Today's tasks
                print(f'Today {self.today.day} {self.mon}:')
                self.rows = session.query(Task). \
                    filter(Task.deadline == self.today.date()).all()
            if user_choice == 3:  # All tasks
                print("All tasks:")
                self.rows = session.query(Task).\
                    order_by(Task.deadline).all()
            if user_choice == 4:
                print("Missed tasks:")
                self.rows = session.query(Task). \
                    filter(Task.deadline < self.today.date()). \
                    order_by(Task.deadline).all()
            if user_choice == 6:
                print("Choose the number of the task you want to delete:")
                self.rows = session.query(Task). \
                    filter(Task.deadline). \
                    order_by(Task.deadline).all()
                self.single_task()
                self.delete()
            self.single_task()

    def single_task(self):
        if len(self.rows) == 0:
            if self.user_choice in [1, 2, 3]:
                print("Nothing to do!")
            if self.user_choice == 4:
                print("Nothing is missed!")
            if self.user_choice == 6:
                print("Nothing to delete!")
        else:
            for row in self.rows:
                if self.user_choice in [1, 2]:
                    print(f"{row.id}. {row.task}")
                elif self.user_choice in [3, 4]:
                    print(f"{row.id}. {row.task}. {row.deadline.strftime('%d')} {row.deadline.strftime('%b')}")
        print()

    def add(self):
        print('Enter task')
        new_task = input()
        print('Enter deadline')
        input_date = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Task(task=new_task, deadline=input_date)
        session.add(new_row)
        session.commit()
        print('The task has been added!')

    def delete(self, delete_row_id=None):
        delete_row_id = int(input())-1
        delete_rows = self.rows[delete_row_id]
        session.delete(delete_rows)
        session.commit()
        print("The task has been deleted!")


todo_list = Todo()
todo_list.user_action()

