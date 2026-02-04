from flask import Flask, request, jsonify
import re

app = Flask(__name__)


@app.route('/add', methods=['GET'])
def add():
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)

    # Validate inputs
    if not a or not b:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Check if inputs are valid numbers (including decimals and negative numbers)
    if not re.match(r'^-?\d+(\.\d+)?$', a) or not re.match(r'^-?\d+(\.\d+)?$', b):
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400

    a_num = float(a)
    b_num = float(b)

    # BUGFIX: The /add endpoint must return the sum of the inputs.
    # A recent change unintentionally used multiplication which breaks the API contract
    # and the Postman/Newman tests (e.g. 5 + 3 should be 8, not 15).
    result = a_num + b_num

    return jsonify({
        'a': a_num,
        'b': b_num,
        'operation': 'addition',
        'result': result
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
