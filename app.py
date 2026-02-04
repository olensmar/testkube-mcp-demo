from flask import Flask, request, jsonify

app = Flask(__name__)

class Calculator:
    def add(self, a, b):
        # NOTE:
        # The `/add` endpoint is used by the Postman/Newman collection executed in
        # the `calculator-addition-test` TestWorkflow.
        #
        # A recent change introduced an intentional bug where `add()` returned
        # multiplication instead of addition, causing workflow execution
        # `calculator-addition-test-9` to fail with:
        #   - expected 15 to deeply equal 8
        #   - expected 4.25 to be close to 4.2
        #
        # Correct behavior is to return the sum of the two numbers.
        return a + b

calculator = Calculator()

@app.route('/add', methods=['GET'])
def add_numbers():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        result = calculator.add(a, b)
        return jsonify({"a": a, "b": b, "operation": "addition", "result": result})
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
