
# TODO
# [+] - crud projects
# [+] - crud tasks
#  [+] - create
#  [+] - put
# [?] - validate args in crud
# [+] - model tasks
# [+] - model projects
# [] - tests
#  [+] - projects
#  [+] - tasks
# [+] - fabrics
# [+] - SQLAlchemy (fastapi tutorial)
# [] - new models
# [] - color in Choices
# [] - migrations (Alembic)
# [] - повторяющийся код убрать (список-деталка Проекта/Тасков)  # TODO next 2
# [+] - Project change and delete DB
#       [+] - change
#       [+] - delete
# [] - расширенный лист (таски + проекты)
# [] - black
# [] - isort
# [+] - структура приложения как в туториале


# db_projects: list[Project] = [
#     Project(
#         id=1,
#         title="Project 1",
#         color="purple",
#         is_active=True,
#     ),
#     Project(
#         id=2,
#         title="Project 2",
#         color="blue",
#         is_active=False,
#     ),
# ]

# db_labels: list[Label] = [
#     Label(
#         id=1,
#         title="Label 1",
#         color="green",
#     ),
#     Label(
#         id=1,
#         title="Label 1",
#         color="green",
#     ),
# ]

# db_tasks: list[Task] = [
#     Task(
#         id=1,
#         title="Task 1",
#         description="Description 1",
#     ),
#     Task(
#         id=2,
#         title="Task 2",
#         description="Description 2",
#         is_checked=True,
#         project=db_projects[0],
#         # labels=[db_labels[0], db_labels[1]]
#     ),
# ]


# db_subtasks: list[Subtask] = [
#     Subtask(
#         id=1,
#         title="Subtask 1",
#         description="Sub Description 1",
#         is_checked=True,
#         task=db_tasks[0],
#     ),
#     Subtask(
#         id=2,
#         title="Subtask 2",
#         description="Sub Description 2",
#         is_checked=True,
#         task=db_tasks[0],
#     ),
# ]
