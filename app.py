from flask import Flask, request, jsonify

app = Flask(__name__)

# Calculator Service
@app.route('/add', methods=['GET'])
def add():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))

        # FIX: perform addition (not multiplication)
        result = a + b

        return jsonify({
            "a": a,
            "b": b,
            "operation": "addition",
            "result": result
        })
    except ValueError:
        return jsonify({
            "error": "Invalid input: both parameters must be numbers"
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
