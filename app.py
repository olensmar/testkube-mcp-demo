from flask import Flask, request, jsonify

def create_app():
    app = Flask(__name__)

    @app.get('/add')
    def add():
        """Add two numbers.

        The Postman collection used by the `calculator-addition-test` workflow expects:
        - 5 + 3 = 8
        - 2.5 + 1.7 = 4.2

        Previous behavior incorrectly returned:
        - 15 for 5 and 3 (likely due to wrong formula)
        - 4.25 for 2.5 and 1.7 (weighted average / wrong rounding)

        To avoid float precision surprises, we compute the result via Decimal and
        then serialize back to float for JSON output.
        """
        from decimal import Decimal, InvalidOperation

        a_raw = request.args.get('a')
        b_raw = request.args.get('b')

        try:
            a = Decimal(a_raw)
            b = Decimal(b_raw)
        except (InvalidOperation, TypeError):
            return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400

        result = a + b

        return jsonify({
            "a": float(a),
            "b": float(b),
            "operation": "addition",
            "result": float(result),
        })

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8080)
