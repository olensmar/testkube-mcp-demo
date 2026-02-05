from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET'])
def add():
    """Add two numbers.

    This endpoint is exercised by the Postman collection in:
    - tests/calculator-addition.postman_collection.json

    The test expectations are:
    - /add?a=5&b=3 => result == 8
    - /add?a=2.5&b=1.7 => result ~= 4.2

    A previous change accidentally used multiplication for the `result`.
    That made the API return 15 and 4.25 respectively, causing the
    workflow `calculator-addition-test` to fail.
    """

    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400

    # Correct behavior: addition
    result = a + b

    return jsonify({'a': a, 'b': b, 'operation': 'addition', 'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
