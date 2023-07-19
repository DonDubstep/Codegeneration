import os
from tasks_for_passak import tasks
for dir in range(len(tasks)):
    folder_name = "./Tests/Test{}".format(dir)
    os.makedirs(folder_name, exist_ok=True)

