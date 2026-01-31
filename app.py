
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/api/calcTax", methods=["POST"])
def calcTax():
  """
  Expects JSON like: {"a": <number>, "b": <number>}
  Returns: {"tax": <number>}
  """
  data = request.get_json(silent=True)

  if not data or "a" not in data or "b" not in data:
    return jsonify({"error1": "Income can not be blank"}), 400
  

  try:
    a = float(data["a"])
    b = float(data["b"])

    if a < 0:
      return jsonify({"error2": "Please provide positive income"}), 400
  
    if b < 1000:
      return jsonify({"taxIncome": 20/100*a, "taxSavings": 0}), 200
    
    return jsonify({"taxIncome": 20/100*a, "taxSavings": 15/100*(b-1000)}), 200
    
  except (ValueError, TypeError):
    return jsonify({"error4": "Both incomes must be numerical"}), 400

  
@app.route("/api/saveTax", methods=["POST"])
def commit_sum():
  data = request.get_json(silent=True)
  
  try:
    a = float(data["a"])
    b = float(data["b"])
    
    # this is where we save the inputs in a db

    return jsonify({"message": "Saved"}), 200
    
  except (ValueError, TypeError):
    return jsonify({"error": "Error saving"}), 400


if __name__ == "__main__":
    app.run(debug=True)
