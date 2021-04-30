""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
import utils
import json

search_result = None

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

@app.route('/summoners')
def summoners():
    keys, items = db_helper.fetch_summoners()
    return render_template('table.html', table_name='Summoners', keys=keys, items=items)

@app.route('/champion_mastery')
def champion_mastery():
    keys, items = db_helper.fetch_champion_mastery()
    return render_template('table2.html', table_name='Champion-Mastery', keys=keys, items=items, advQuery='/ethanQuery', graph_bar='/bar')

@app.route('/matches')
def matches():
    keys, items = db_helper.fetch_matches()
    return render_template('table.html', table_name='matches', keys=keys, items=items, advQuery='/ryanQuery')

@app.route("/delete/<string:keys>", methods=['POST'])
def delete(keys):
    data = request.get_json()
    data = utils.fix_nesting(data)
    data = json.loads(data)

    table = utils.hyphen_to_camel(data['table'])
    try:
        db_helper.remove_row_by_pk(table, keys)
        result = {'success': True, 'response': 'Removed row'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/edit", methods=['POST'])
def update():
    """ recieved post requests for entry updates """
    # utils.debug_log('here')
    data = request.get_json()
    # utils.debug_log(str(data))

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
    # utils.debug_log(str(data))

    try:
        db_helper.create_row(data)
        result = {'success': True, 'response': 'Done'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/search", methods=['POST'])
def search():
    data = request.get_json()
    # # utils.debug_log(str(data))
    data = utils.fix_nesting(data)
    data = json.loads(data)
    
    try:
        keys, items = db_helper.search(data)
        global search_result
        search_result = (data['table'], keys, items)
        # utils.debug_log(str(search_result))
        result = {'success': True, 'response': 'Done'}
    except Exception as e:
        # utils.debug_log(str(e))
        result = {'success': False, 'response': f'Something went wrong'}

    return jsonify(result)

@app.route("/searchResults")
def search_results():
    table = search_result[0]
    # utils.debug_log(table)
    return render_template('table.html', table_name=table, keys=search_result[1], items=search_result[2])

@app.route("/mattQuery")
def matt_query():
    keys, items = db_helper.adv_query_match_history()
    return render_template('table.html', table_name='Match-History', keys=keys, items=items, advQuery="/mattQuery")
    
@app.route("/hskQuery")
def hsk_query():
    keys, items = db_helper.adv_query_champions()
    return render_template('table.html', table_name='champions', keys=keys, items=items, advQuery="/hskQuery")

@app.route("/ethanQuery")
def ethan_query():
    keys, items = db_helper.adv_query_champion_mastery()
    return render_template('table2.html', table_name='Champion-Mastery', keys=keys, items=items, advQuery="/ethanQuery")

@app.route("/ryanQuery")
def ryan_query():
    keys, items = db_helper.Ryan_adv_query_matches()
    return render_template('table.html', table_name='matches', keys=keys, items=items, advQuery="/ryanQuery")

@app.route('/bar')
def bar():
    keys, items = db_helper.adv_query_champion_mastery()
    champ_id_list = []
    avg_dmg_list = []
    for item in items:
        champ_id_list.append(list(item.values())[0])
        avg_dmg_list.append(list(item.values())[1])
    print(champ_id_list)
    return render_template('chart.html', title='Average Damage', max=200000, labels=champ_id_list, values=avg_dmg_list, graph_bar="/bar")

@app.route('/storedProcedure', methods=['POST'])
def stored_procedure():
    data = request.get_json()
    # utils.debug_log('here')
    # utils.debug_log(str(data))
    data = utils.fix_nesting(data)
    # utils.debug_log(str(data))
    data = json.loads(data)

    try:
        keys, items = db_helper.call_stored_procedure(data['param'])
        global procedure_results
        procedure_results = (keys, items)
        # utils.debug_log(str(procedure_results))
        result = {'success': True, 'response': 'Done'}
    except Exception as e:
        # utils.debug_log(str(e))
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route('/procedureResults')
def procedure_results():
    return render_template('table.html', table_name='Procedure Results', keys=procedure_results[0], items=procedure_results[1])
