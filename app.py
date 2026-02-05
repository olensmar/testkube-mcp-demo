from flask import Flask, request, jsonify

app = Flask(__name__)


class Calculator:
    def add(self, a, b):
        # NOTE:
        # The calculator-addition Postman collection expects true arithmetic addition.
        # A previous change accidentally (re)introduced multiplication here, causing:
        #   5 + 3 => 15
        #   2.5 + 1.7 => 4.25
        # which matches the observed failing Testkube execution.
        return a + b


calculator = Calculator()


@app.route('/add')
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400

    result = calculator.add(a, b)
    return jsonify({
        "a": a,
        "b": b,
        "operation": "addition",
        "result": result
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
