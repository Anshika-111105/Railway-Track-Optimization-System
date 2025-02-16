from flask import Flask, request, jsonify

app = Flask(__name__)

# List of available stations (Can be fetched from a database)
stations = ["New Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"]

@app.route('/stations', methods=['GET'])
def get_stations():
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)
