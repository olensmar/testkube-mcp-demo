from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/add')
def add():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
        result = a + b  # fixed: addition, not multiplication
        return jsonify({'a': a, 'b': b, 'operation': 'addition', 'result': result})
    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
