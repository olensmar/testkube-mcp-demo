from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/add')
def add():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))

        # NOTE:
        # The /add endpoint must return the SUM of the provided parameters.
        # A recent change accidentally returned a*b which breaks the Postman
        # collection used by Testkube workflow `calculator-addition-test`.
        result = a + b

        return jsonify({
            'a': a,
            'b': b,
            'operation': 'addition',
            'result': result
        })
    except ValueError:
        return jsonify({'error': 'Invalid input: both parameters must be numbers'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
