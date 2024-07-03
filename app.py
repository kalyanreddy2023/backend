from flask import Flask, request, jsonify
import operara
import piafacts

app = Flask(__name__)

@app.route('/piafacts/', methods=['GET'])
def get_piafacts():
    try:
        item_codes = request.args.get('item_code')
        if item_codes is None:
            return jsonify({'error': 'Both item_code. Please provide them in the query parameters.'}), 400
        result = piafacts.get_data(item_codes)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/operera/', methods=['GET'])
def get_operara():
    try:
        item_codes = request.args.get('item_code')
        country_code = request.args.get('country_code')
        if item_codes is None or country_code is None:
            return jsonify({'error': 'Both item_code and country_code are required. Please provide them in the query parameters.'}), 400
        result = operara.get_data(item_codes, country_code)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, use_reloader=True)
