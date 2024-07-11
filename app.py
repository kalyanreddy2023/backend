from flask import Flask, request, jsonify
import operara
import piafacts

app = Flask(__name__)

@app.route('/piafacts/', methods=['GET'])
def get_piafacts():
    try:
        item_code = request.args.get('item_code')
        if not item_code:
            return jsonify({'error': 'item_code parameter is required.'}), 400
        
        result = piafacts.get_data(item_code)
        if not result:
            return jsonify({'error': 'No data found for item_code: {}'.format(item_code)}), 404
        
        return jsonify(result), 200
    
    except Exception as e:
        print(e)  # Log the exception for debugging purposes
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/operera/', methods=['GET'])
def get_operara():
    try:
        item_code = request.args.get('item_code')
        country_code = request.args.get('country_code')
        
        if not item_code or not country_code:
            return jsonify({'error': 'Both item_code and country_code parameters are required.'}), 400
        
        result = operara.get_data(item_code, country_code)
        if not result:
            return jsonify({'error': 'No data found for item_code: {} and country_code: {}'.format(item_code, country_code)}), 404
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=8080, host="0.0.0.0", threaded=True)
