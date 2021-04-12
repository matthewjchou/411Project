from app import db
import utils
from utils import debug_log
import json

def fetch_tables():
    conn = db.connect()
    result = conn.execute('SHOW TABLES')
    conn.close()

    items = []
    for r in result:
        n = utils.camel_to_normal(r[0])
        item = {
            "name": n,
            "link": '/' + utils.normal_to_snake(n)
        }
        items.append(item)

    return items

def fetch_champions():
    conn = db.connect()
    result = conn.execute('SELECT * FROM champions LIMIT 20').fetchall()
    conn.close()

    items = []
    for r in result:
        debug_log(str(r))
    return items

def fetch_match_history():
    conn = db.connect()
    result = conn.execute('SELECT * FROM matchHistory LIMIT 20')
    conn.close()
    
    pk = ['AccountId', 'GameId']
    keys, items = utils.result_to_dict(result, pk)
    return keys, items

def remove_row_by_pk(table, pks):
    pks = pks.replace("'", '"')
    pks = json.loads(pks)
    id = ""
    for k, v in pks.items():
        if any(c.isalpha() for c in str(v)):
            id += f'{k}="{v}" AND '
        else:
            id += f'{k}={v} AND '
    id = id[:-5]

    conn = db.connect()
    query = f'DELETE FROM {table} WHERE {id};'
    utils.debug_log(query)
    conn.execute(query)
    conn.close()

# example code below:

# def fetch_todo() -> dict:
#     """Reads all tasks listed in the todo table

#     Returns:
#         A list of dictionaries
#     """

#     conn = db.connect()
#     query_results = conn.execute("Select * from tasks;").fetchall()
#     conn.close()
#     todo_list = []
#     for result in query_results:
#         item = {
#             "id": result[0],
#             "task": result[1],
#             "status": result[2]
#         }
#         todo_list.append(item)

#     return todo_list


# def update_task_entry(task_id: int, text: str) -> None:
#     """Updates task description based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated description

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def update_status_entry(task_id: int, text: str) -> None:
#     """Updates task status based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated status

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


# def insert_new_task(text: str) ->  int:
#     """Insert new task to todo table.

#     Args:
#         text (str): Task description

#     Returns: The task ID for the inserted entry
#     """

#     conn = db.connect()
#     query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
#         text, "Todo")
#     conn.execute(query)
#     query_results = conn.execute("Select LAST_INSERT_ID();")
#     query_results = [x for x in query_results]
#     task_id = query_results[0][0]
#     conn.close()

#     return task_id


# def remove_task_by_id(task_id: int) -> None:
#     """ remove entries based on task ID """
#     conn = db.connect()
#     query = 'Delete From tasks where id={};'.format(task_id)
#     conn.execute(query)
#     conn.close()
