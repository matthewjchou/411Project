from app import db
import utils
from utils import debug_log
import json

match_history_pks = ['AccountId', 'GameId']
champion_mastery_pks = ['SummonerId']
champ_pk = ['DataKey']
match_pk = ['GameId']
summoners_pk = ['AccountId']
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

def fetch_champion_mastery():
    conn = db.connect()
    result = conn.execute('SELECT * FROM championMastery LIMIT 100')
    conn.close()
    
    keys, items = utils.result_to_dict(result, champion_mastery_pks)
    return keys, items

def fetch_champions():
    conn = db.connect()
    result = conn.execute('SELECT * FROM champions')
    conn.close()

    keys, items = utils.result_to_dict(result, champ_pk)
    return keys, items

def fetch_match_history():
    conn = db.connect()
    result = conn.execute('SELECT * FROM matchHistory LIMIT 100')
    conn.close()
    
    keys, items = utils.result_to_dict(result, match_history_pks)
    return keys, items

def fetch_matches():
    conn = db.connect()
    result = conn.execute('SELECT * FROM matches LIMIT 100')
    conn.close()

    keys, items = utils.result_to_dict(result, match_pk)
    return keys, items

def fetch_summoners():
    conn = db.connect()
    result = conn.execute('SELECT * FROM summoners LIMIT 100')
    conn.close()

    keys, items = utils.result_to_dict(result, summoners_pk)
    return keys, items

def remove_row_by_pk(table, pks):
    id = utils.generate_where_from_pk(pks)

    conn = db.connect()
    query = f'DELETE FROM {table} WHERE {id};'
    conn.execute(query)
    conn.close()

def create_row(data):
    data = utils.fix_nesting(data)
    data = json.loads(data)
    
    table = data['table']
    table = utils.hyphen_to_camel(table)
    fields, keys, vals = utils.generate_fields(data)
    # utils.debug_log(str(fields))

    conn = db.connect()
    query = f'INSERT INTO {table} ({keys}) VALUES ({vals})'
    # utils.debug_log(query)
    conn.execute(query)
    conn.close()


def update_row(data):
    data = utils.fix_nesting(data)
    data = json.loads(data)

    pks = data['pk']
    id = utils.generate_where_from_pk(pks)
    # utils.debug_log(id)

    table = data['table']
    table = utils.hyphen_to_camel(table)
    fields, k, v = utils.generate_fields(data)
    # utils.debug_log(str(fields))

    conn = db.connect()
    query = f'UPDATE {table} SET {fields} WHERE {id};'
    # utils.debug_log(query)
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
    # utils.debug_log(query)
    result = conn.execute(query)
    conn.close()

    pk = []

    if table == 'matchHistory':
        pk = match_history_pks
    elif table == 'championMastery':
        pk = champion_mastery_pks
    elif table == 'champions':
        pk = champ_pk
    elif table == 'matches':
        pk = match_pk
    elif table == 'summoners':
        pk = summoners_pk

    k, i = utils.result_to_dict(result, pk)

    return k, i

def adv_query_match_history():
    conn = db.connect()
    result = conn.execute('SELECT (SELECT Name FROM summoners s WHERE s.AccountId = m.AccountId) AS Name, COUNT(DISTINCT Champion) AS Num_Champions FROM matchHistory m GROUP BY AccountId LIMIT 100;')
    conn.close()
    
    keys = ['Name', 'Num_Champions']
    result = result.fetchall()  
    items = [dict(zip(keys, row)) for row in result]
 
    return keys, items


def adv_query_champions():
    conn = db.connect()
    result = conn.execute('SELECT (SELECT Name FROM summoners s WHERE s.AccountId = m.AccountId) AS summoner, m.Champion AS championChar, c.DataName AS champDName FROM matchHistory m JOIN champions c ON m.Champion = c.DataKey ORDER BY (SELECT Name FROM summoners s WHERE s.AccountId = m.AccountId) ASC LIMIT 15;')
    conn.close()
    
    keys = ['summoner', 'championChar', 'champDName']
    result = result.fetchall()
    items = [dict(zip(keys, row)) for row in result]

    return keys, items

def adv_query_champion_mastery():
    conn = db.connect()
    result = conn.execute('SELECT championId, AVG(ChampionPoints) AS avgDamage FROM championMastery c JOIN summoners s ON c.SummonerId = s.Id WHERE Tier = "Challenger" GROUP BY ChampionId LIMIT 15;')
    conn.close()
    
    keys = ['championId', 'avgDamage']
    result = result.fetchall()  
    items = [dict(zip(keys, row)) for row in result]

    return keys, items

def Ryan_adv_query_matches():
    conn = db.connect()
    result = conn.execute('SELECT m.AccountID AS ID, avg(m.Timestamp) as AvgPlayTime FROM matchHistory m join summoners s on m.AccountID = s.AccountID WHERE s.Tier = "Challenger" GROUP BY m.AccountID ORDER BY AvgPlayTime DESC limit 15;')
    conn.close()

    keys = ['ID', 'AvgPlayTime']
    result = result.fetchall()
    items = [dict(zip(keys, row)) for row in result]

    return keys, items

def call_stored_procedure(param):
    conn = db.connect()
    result = conn.execute(f"CALL getAvgPlayTimes('{param.upper()}')")
    conn.close()

    keys = ['AccountId', 'PlayTime', 'LanePhase', 'GamePlayStatus']
    result = result.fetchall()
    items = [dict(zip(keys, row)) for row in result]
    # for i in items:
        # utils.debug_log(str(i))
    return keys, items

