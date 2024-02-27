import json
from flask import Flask, jsonify, request, abort

app = Flask('app')


@app.route('/')
def hello_world():
    return 'Welcome to Vivisteria! '


@app.route('/states', methods=['GET', 'POST', 'PUT'])
def get_state():
    states = get_states()
    if request.method == 'GET':
        if 'search' in request.args:
            search = request.args['search']
            search_term = []
            for state in states:
                if search in state['name']:
                    search_term.append(state)
            return jsonify(search_term)

        return jsonify(states)

    if request.method == 'POST':
        data = request.json
        states.append(data)
        overwrite_saved_data(states)
        return ({'message': "State added!"})

    if request.method == 'PUT':
        data = request.json
        for state in states:
            if state['id'] == data['id']:
                states.remove(state)
                states.append(data)
        overwrite_saved_data(states)
        return ({'message': "State updated!"})


@app.route('/states/<status>', methods=['GET'])
def get_state_by_status(status):
    states = get_states()
    status_list = []
    valid_status = ["Special Capital Territory",
                    "Union Territory", "State", "Oversea Territory"]
    if status not in valid_status:
        raise ValueError(
            "The status must be valid (either Special Capital Territory, Union Territory, State or Oversea Territory)")
    for state in states:
        if status == state['status']:
            status_list.append(state)
    return jsonify(status_list)


@app.route('/states/<int:id>', methods=['GET'])
def get_state_by_id(id):
    states = get_states()
    for state in states:
        if state['id'] == id:
            return jsonify(state)
    abort(404)


def get_states():
    with open('states.json', 'r', encoding="utf-8") as f:
        return json.load(f)


def overwrite_saved_data(new_data):
    """Overwrites saved data."""
    with open("states.json", "w", encoding="utf-8") as file:
        return json.dump(new_data, file, indent=6)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
