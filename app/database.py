from app import db
import utils
from utils import debug_log
import json

match_history_pks = ['AccountId', 'GameId']
champions_pks = []
search_results = None


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
    return items

def fetch_match_history():
    conn = db.connect()
    result = conn.execute('SELECT * FROM matchHistory LIMIT 20')
    conn.close()
    
    keys, items = utils.result_to_dict(result, match_history_pks)
    return keys, items


def fetch_champion_mastery():
    conn = db.connect()
    result = conn.execute('SELECT * FROM championMastery LIMIT 20')
    conn.close()
    
    keys, items = utils.result_to_dict(result, match_history_pks)
    return keys, items

def remove_row_by_pk(table, pks):
    id = utils.generate_where_from_pk(pks)

    conn = db.connect()
    query = f'DELETE FROM {table} WHERE {id};'
    utils.debug_log(query)
    conn.execute(query)
    conn.close()

def create_row(data):
    data = utils.fix_nesting(data)
    data = json.loads(data)
    
    table = data['table']
    table = utils.hyphen_to_camel(table)
    fields, keys, vals = utils.generate_fields(data)
    utils.debug_log(str(fields))

    conn = db.connect()
    query = f'INSERT INTO {table} ({keys}) VALUES ({vals})'
    utils.debug_log(query)
    conn.execute(query)
    conn.close()


def update_row(data):
    data = utils.fix_nesting(data)
    data = json.loads(data)

    pks = data['pk']
    id = utils.generate_where_from_pk(pks)
    utils.debug_log(id)

    table = data['table']
    table = utils.hyphen_to_camel(table)
    fields, k, v = utils.generate_fields(data)
    utils.debug_log(str(fields))

    conn = db.connect()
    query = f'UPDATE {table} SET {fields} WHERE {id};'
    utils.debug_log(query)
    conn.execute(query)
    conn.close()

def search(data):
    table = data['table']
    table = utils.hyphen_to_camel(table)
    keyword = data['keyword']

    keys = data['keys']
    searches = utils.generate_searches(keys, keyword)

    conn = db.connect()
    query = f'SELECT * FROM {table} WHERE {searches};'
    utils.debug_log(query)
    result = conn.execute(query)
    conn.close()

    pk = []
    if table == 'matchHistory':
        pk = match_history_pks
    elif table == 'champions':
        pk = champions_pks

    k, i = utils.result_to_dict(result, pk)

    return k, i

def adv_query_match_history():
    utils.debug_log("here2")
    conn = db.connect()
    result = conn.execute('SELECT (SELECT Name FROM summoners s WHERE s.AccountId = m.AccountId) AS Name, COUNT(DISTINCT Champion) AS Num_Champions FROM matchHistory m GROUP BY AccountId LIMIT 100;')
    conn.close()
    
    keys = ['Name', 'Num_Champions']
    result = result.fetchall()  
    items = [dict(zip(keys, row)) for row in result]
    for i in items:
        utils.debug_log(str(i))
    return keys, items

def adv_query_champion_mastery():
    conn = db.connect()
    result = conn.execute('SELECT championId, AVG(ChampionPoints) AS avgDamage FROM championMastery c JOIN summoners s ON c.SummonerId = s.Id WHERE Tier = "Challenger" GROUP BY ChampionId LIMIT 15;')
    conn.close()
    
    keys = ['championId', 'avgDamage']
    result = result.fetchall()  
    items = [dict(zip(keys, row)) for row in result]
    for i in items:
        utils.debug_log(str(i))
    return keys, items
    

    
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
