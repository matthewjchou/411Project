""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
import utils
import json

search_results = None

@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_tables()
    return render_template("index.html", items=items)

@app.route('/champions')
def champions():
    keys, items = db_helper.fetch_champions()
    return render_template('table.html', table_name='champions', keys=keys, items=items,advQuery='/hskQuery')

@app.route('/match_history')
def match_history():
    keys, items = db_helper.fetch_match_history()
    return render_template('table.html', table_name='Match-History', keys=keys, items=items, advQuery='/mattQuery')

@app.route('/champion_mastery')
def champion_mastery():
    keys, items = db_helper.fetch_champion_mastery()
    return render_template('table2.html', table_name='Champion-Mastery', keys=keys, items=items, advQuery='/ethanQuery', graph_bar='/bar')

@app.route('/matches')
def matches():
    keys, items = db_helper.fetch_matches()
    return render_template('table.html', table_name='matches', keys=keys, items=items, advQuery='/ryanQuery')

@app.route('/summoners')
def summoners():
    return render_template('table.html', table_name='Summoners')

@app.route("/delete/<string:keys>", methods=['POST'])
def delete(keys):
    """ recieved post requests for entry delete """
    utils.debug_log(str(keys))
    split = keys.split('|')
    table = utils.hyphen_to_camel(split[0])
    try:
        db_helper.remove_row_by_pk(table, split[1])
        result = {'success': True, 'response': 'Removed row'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/edit", methods=['POST'])
def update():
    """ recieved post requests for entry updates """
    utils.debug_log('here')
    data = request.get_json()
    utils.debug_log(str(data))

    try:
        db_helper.update_row(data)
        result = {'success': True, 'response': 'Status Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    utils.debug_log(str(data))

    try:
        db_helper.create_row(data)
        result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/search", methods=['POST'])
def search():
    data = request.get_json()
    utils.debug_log(str(data))
    data = utils.fix_nesting(data)
    data = json.loads(data)
    
    try:
        keys, items = db_helper.search(data)
        global search_results
        search_results = (data['table'], keys, items)
        utils.debug_log(str(search_results))
        result = {'success': True, 'response': 'Done'}
    except Exception as e:
        utils.debug_log(str(e))
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/searchResults")
def search_results():
    table = search_results[0]
    utils.debug_log(table)
    return render_template('table.html', table_name=table, keys=search_results[1], items=search_results[2])

@app.route("/mattQuery")
def matt_query():
    utils.debug_log('here1')
    keys, items = db_helper.adv_query_match_history()
    return render_template('table.html', table_name='Match-History', keys=keys, items=items, advQuery="/mattQuery")
    
@app.route("/hskQuery")
def hsk_query():
    utils.debug_log('being called')
    keys, items = db_helper.adv_query_champions()
    return render_template('table.html', table_name='champions', keys=keys, items=items, advQuery="/hskQuery")

@app.route("/ethanQuery")
def ethan_query():
    utils.debug_log('being called')
    keys, items = db_helper.adv_query_champion_mastery()
    return render_template('table2.html', table_name='Champion-Mastery', keys=keys, items=items, advQuery="/ethanQuery")

@app.route("/ryanQuery")
def ryan_query():
    utils.debug_log('being called')
    keys, items = db_helper.Ryan_adv_query_matches()
    return render_template('table.html', table_name='matches', keys=keys, items=items, advQuery="/ryanQuery")

@app.route('/bar')
def bar():
    utils.debug_log('hello')
    keys, items = db_helper.adv_query_champion_mastery()
    champ_id_list = []
    avg_dmg_list = []
    for item in items:
        champ_id_list.append(list(item.values())[0])
        avg_dmg_list.append(list(item.values())[1])
    print(champ_id_list)
    return render_template('chart.html', title='Average Damage', max=200000, labels=champ_id_list, values=avg_dmg_list, graph_bar="/bar")

# Example code below:

# @app.route("/delete/<int:task_id>", methods=['POST'])
# def delete(task_id):
#     """ recieved post requests for entry delete """

#     try:
#         db_helper.remove_task_by_id(task_id)
#         result = {'success': True, 'response': 'Removed task'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     """ recieved post requests for entry updates """

#     data = request.get_json()

#     try:
#         if "status" in data:
#             db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#             db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}

#     return jsonify(result)


# @app.route("/create", methods=['POST'])
# def create():
#     """ recieves post requests to add new task """
#     data = request.get_json()
#     db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)
