from flask import Flask, request, jsonify

app = Flask(__name__)

def fibonacci(n):
    if n <= 0:
        return []
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

@app.route('/api/fibonacci', methods=['GET'])
def get_fibonacci():
    try:
        n = int(request.args.get('n', 10))
        result = fibonacci(n)
        return jsonify({'fibonacci': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)