""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_tables()
    return render_template("index.html", items=items)

@app.route('/champions')
def champions():
    # items = db_helper.fetch_champions()
    return render_template('table.html', table_name='Champions', items=items)

@app.route('/match_history')
def match_history():
    keys, items = db_helper.fetch_match_history()
    return render_template('table.html', table_name='Match History', keys=keys, items=items)

@app.route('/champion_mastery')
def champion_mastery():
    return render_template('table.html', table_name='Champion Mastery')

@app.route('/matches')
def matches():
    return render_template('table.html', table_name='Matches')

@app.route('/summoners')
def summoners():
    return render_template('table.html', table_name='Summoners')

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
