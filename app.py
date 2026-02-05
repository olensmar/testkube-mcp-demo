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
    """Add two numbers and return the result.

    NOTE: This endpoint is expected to perform **addition**, not any
    other operation. External tests like the `calculator-addition-test`
    Postman collection assume:

      - 5 + 3 = 8
      - 2.5 + 1.7 = 4.2

    If this implementation is accidentally changed to use
    multiplication (a * b) or any other operation, those tests will
    fail (e.g. 5 * 3 = 15, 2.5 * 1.7 = 4.25). This docstring is here
    to make that contract explicit and help prevent regressions.
    """
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))

        # FIX: perform actual addition instead of multiplication
        result = a + b

        action_history.append({"operation": "addition", "a": a, "b": b, "result": result})
        return jsonify({"a": a, "b": b, "operation": "addition", "result": result})
    except ValueError:
        logging.error("Invalid input for addition: a=%s, b=%s", request.args.get("a"), request.args.get("b"))
        return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400


@app.route("/subtract")
@simulate_latency
def subtract():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        result = a - b
        action_history.append({"operation": "subtraction", "a": a, "b": b, "result": result})
        return jsonify({"a": a, "b": b, "operation": "subtraction", "result": result})
    except ValueError:
        logging.error("Invalid input for subtraction: a=%s, b=%s", request.args.get("a"), request.args.get("b"))
        return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400


@app.route("/multiply")
@simulate_latency
def multiply():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        result = a * b
        action_history.append({"operation": "multiplication", "a": a, "b": b, "result": result})
        return jsonify({"a": a, "b": b, "operation": "multiplication", "result": result})
    except ValueError:
        logging.error("Invalid input for multiplication: a=%s, b=%s", request.args.get("a"), request.args.get("b"))
        return jsonify({"error": "Invalid input: both parameters must be numbers"}), 400


@app.route("/divide")
@simulate_latency
def divide():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 1))
        if b == 0:
            logging.warning("Division by zero attempted: a=%s, b=%s", a, b)
            return jsonify({"error": "Division by zero is not allowed"}), 400

        result = a / b
        action_history.append({"operation": "division", "a": a, "b": b, "result": result})
        return jsonify({"a": a, "b": b, "operation": "division", "result": result})
    except ValueError:
        logging.error("Invalid input for division: a=%s, b=%s", request.args.get("a"), request.args.get("b"))
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
