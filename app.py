from flask import Flask, request, jsonify
import re

app = Flask(__name__)


def sanitize_input(input_str):
    """Sanitize user input to prevent injection attacks."""
    # Only allow numbers, decimal points, and optional negative sign
    if not re.match(r'^-?\d*\.?\d+$', str(input_str)):
        return None
    return float(input_str)


@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Calculator Service</title>
        </head>
        <body>
            <h1>Calculator Service</h1>
            <p>Available endpoints:</p>
            <ul>
                <li><a href="/add?a=5&b=3">/add?a=5&b=3</a></li>
                <li><a href="/subtract?a=10&b=4">/subtract?a=10&b=4</a></li>
                <li><a href="/multiply?a=6&b=7">/multiply?a=6&b=7</a></li>
                <li><a href="/divide?a=20&b=5">/divide?a=20&b=5</a></li>
            </ul>
        </body>
    </html>
    """


@app.route('/add')
def add():
    try:
        a = request.args.get('a', 0)
        b = request.args.get('b', 0)

        a_value = sanitize_input(a)
        b_value = sanitize_input(b)

        if a_value is None or b_value is None:
            raise ValueError("Invalid input")

        result = a_value + b_value  # minimal fix: addition, not multiplication

        return jsonify({
            'a': a_value,
            'b': b_value,
            'operation': 'addition',
            'result': result
        })

    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400


@app.route('/subtract')
def subtract():
    try:
        a = request.args.get('a', 0)
        b = request.args.get('b', 0)

        a_value = sanitize_input(a)
        b_value = sanitize_input(b)

        if a_value is None or b_value is None:
            raise ValueError("Invalid input")

        result = a_value - b_value

        return jsonify({
            'a': a_value,
            'b': b_value,
            'operation': 'subtraction',
            'result': result
        })

    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400


@app.route('/multiply')
def multiply():
    try:
        a = request.args.get('a', 0)
        b = request.args.get('b', 0)

        a_value = sanitize_input(a)
        b_value = sanitize_input(b)

        if a_value is None or b_value is None:
            raise ValueError("Invalid input")

        result = a_value * b_value

        return jsonify({
            'a': a_value,
            'b': b_value,
            'operation': 'multiplication',
            'result': result
        })

    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400


@app.route('/divide')
def divide():
    try:
        a = request.args.get('a', 0)
        b = request.args.get('b', 1)

        a_value = sanitize_input(a)
        b_value = sanitize_input(b)

        if a_value is None or b_value is None:
            raise ValueError("Invalid input")

        if b_value == 0:
            return jsonify({'error': 'Division by zero is not allowed'}), 400

        result = a_value / b_value

        return jsonify({
            'a': a_value,
            'b': b_value,
            'operation': 'division',
            'result': result
        })

    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
