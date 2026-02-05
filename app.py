from flask import Flask, request, jsonify, render_template
import time
import logging
from functools import wraps
from markupsafe import escape

app = Flask(__name__)

# In-memory storage for calculator history
action_history = []

# Logger setup
logging.basicConfig(level=logging.INFO)


# Decorator to simulate latency
#
# This is intentionally kept very small so it doesn't meaningfully
# impact tests or user experience, but allows us to demonstrate
# latency-related issues if needed in the future.
def simulate_latency(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info("Function %s took %s seconds", func.__name__, end_time - start_time)
        return result

    return wrapper


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add")
@simulate_latency
def add():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))

        # FIX: perform actual addition instead of multiplication
        # This endpoint is expected to return the mathematical sum of
        # the two operands so that external tests (for example the
        # `calculator-addition-test` Postman collection used in
        # Testkube) receive:
        #   - 5 + 3 = 8
        #   - 2.5 + 1.7 = 4.2
        # If we accidentally multiply here (a * b), the service will
        # return 15 and 4.25 for the examples above, which makes those
        # tests fail. Keeping this logic explicitly documented should
        # help prevent similar regressions.
        result = a + b

        action_history.append({"operation": "addition", "a": a, "b": b, "result": result})
        return jsonify({"a": a, "b": b, "operation": "addition", "result": result})
    except ValueError:
        logging.error("Invalid input for addition: a=%s, b=%s", request.args.get("a"), request.args.get("b"))
        return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400


@app.route("/history")
def history():
    # Escape potentially unsafe data when rendering
    safe_history = [
        {
            "operation": escape(str(entry.get("operation", ""))),
            "a": escape(str(entry.get("a", ""))),
            "b": escape(str(entry.get("b", ""))),
            "result": escape(str(entry.get("result", ""))),
        }
        for entry in action_history
    ]
    return jsonify(safe_history)


if __name__ == "__main__":
    # Only enable debug mode in development, not in production
    app.run(host="0.0.0.0", port=5000, debug=False)
