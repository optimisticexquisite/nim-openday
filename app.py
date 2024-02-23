from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.secret_key = 'super secret key'

def nim_sum(piles):
    xor = 0
    for pile in piles:
        xor ^= pile
    return xor

def next_move(piles):
    binary = []
    for pile in piles:
        binary.append(bin(pile)[2:])
    max_len = max([len(b) for b in binary])
    for i in range(len(binary)):
        binary[i] = binary[i].zfill(max_len)
    nim = nim_sum(piles)
    if nim != 0:
        nim = bin(nim)[2:].zfill(max_len)
        for i in range(len(binary)):
            if int(binary[i], 2) ^ int(nim, 2) < int(binary[i], 2):
                piles[i] = int(binary[i], 2) ^ int(nim, 2)
                return int(binary[i], 2) - piles[i], i
    else:
        # Remove one coin from the largest pile
        max_pile = max(piles)
        for i in range(len(piles)):
            if piles[i] == max_pile:
                piles[i] -= 1
                return 1, i
    return 1, 0

@app.route('/')
def index():
    return render_template('nim.html')


@app.route('/api/next-move', methods=['POST'])
def api_next_move():
    data = request.json
    piles = data.get('stacks')
    if piles is None:
        return jsonify({'error': 'Missing data'}), 400

    coins_to_remove, stack_number = next_move(piles)
    return jsonify({'coinsToRemove': coins_to_remove, 'stackIndex': stack_number})

if __name__ == '__main__':
    app.run(debug=True)
