
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

def calculate_tax(empl_income, savings_income, bonus_income):
  if empl_income < 25000:
    bonus_rate = 20 / 100
  elif empl_income <= 50000:
    bonus_rate = 40 / 100
  else:
    bonus_rate = 45 / 100

  tax_income = 20 / 100 * empl_income
  tax_bonus = bonus_rate * bonus_income
  if savings_income < 1000:
    tax_savings = 0
  else:
    tax_savings = 15 / 100 * (savings_income - 1000)

  return {"taxIncome": tax_income, "taxSavings": tax_savings, "taxBonus": tax_bonus}

@app.route("/", methods=["GET"])
def home():
  return render_template("index.html")

@app.route("/confirm", methods=["GET"])
def confirm():
  incomes = session.get("incomes")
  return render_template("confirm.html", incomes=incomes)

@app.route("/api/inputs", methods=["POST"])
def save_inputs():
  data = request.get_json(silent=True)

  if not data or "a" not in data or "b" not in data or "c" not in data:
    return jsonify({"error1": "Income can not be blank"}), 400

  try:
    a = float(data["a"])
    b = float(data["b"])
    c = float(data["c"])

    if a < 0 or b < 0 or c < 0:
      return jsonify({"error2": "Please provide positive income"}), 400

    session["incomes"] = {"a": a, "b": b, "c": c}
    return jsonify({"message": "Stored"}), 200
  except (ValueError, TypeError):
    return jsonify({"error4": "Both incomes must be numerical"}), 400

@app.route("/api/confirm", methods=["POST"])
def confirm_tax():
  incomes = session.get("incomes")

  if not incomes:
    return jsonify({"error1": "Income can not be blank"}), 400

  try:
    a = float(incomes["a"])
    b = float(incomes["b"])
    c = float(incomes["c"])
  except (ValueError, TypeError, KeyError):
    return jsonify({"error4": "Both incomes must be numerical"}), 400

  import db_manager
  db_manager.addIncomes(1, a, b, c)

  tax_totals = calculate_tax(a, b, c)
  return jsonify(tax_totals), 200

@app.route("/api/calcTax", methods=["POST"])
def calcTax():
  """
  Expects JSON like: {"a": <number>, "b": <number>, "c": <number>}
  Returns: {"taxIncome": <number>, "taxSavings": <number>, "taxBonus": <number>}
  """
  data = request.get_json(silent=True)

  if not data or "a" not in data or "b" not in data or "c" not in data:
    return jsonify({"error1": "Income can not be blank"}), 400
  

  try:
    a = float(data["a"])
    b = float(data["b"])
    c = float(data["c"])

    if a < 0 or b < 0 or c < 0:
      return jsonify({"error2": "Please provide positive income"}), 400

    tax_totals = calculate_tax(a, b, c)
    return jsonify(tax_totals), 200
    
  except (ValueError, TypeError):
    return jsonify({"error4": "Both incomes must be numerical"}), 400

  
@app.route("/api/saveTax", methods=["POST"])
def commit_sum():
  data = request.get_json(silent=True)
  
  try:
    a = float(data["a"])
    b = float(data["b"])
    
    # this is where we save the inputs in a db
    #import db_manager
    #db_manager.addIncomes(1, a, b)

    return jsonify({"message": "Saved"}), 200
    
  except (ValueError, TypeError):
    return jsonify({"error": "Error saving"}), 400


if __name__ == "__main__":
    app.run(debug=True)
