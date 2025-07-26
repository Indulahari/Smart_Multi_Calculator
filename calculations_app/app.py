from flask import Flask, render_template, request, jsonify
from datetime import datetime
import math
import requests

app = Flask(__name__)

# ---------------- Home ----------------
@app.route('/')
def index():
    return render_template('index.html')


# ---------------- Basic Calculator ----------------
@app.route('/basic-calculator')
def basic_calculator():
    return render_template('basic_calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression', '')

        allowed_chars = "0123456789+-*/.() "
        if any(char not in allowed_chars for char in expression):
            return jsonify({'result': 'Invalid characters'})

        result = eval(expression)
        return jsonify({'result': result})
    except Exception:
        return jsonify({'result': 'Error'})


# ---------------- BMI Calculator ----------------
@app.route("/bmi-calculator", methods=["GET", "POST"])
def bmi_calculator():
    result = None
    category = None
    suggestion = None
    age = None

    if request.method == "POST":
        try:
            age = int(request.form["age"])
            weight = float(request.form["weight"])
            height = float(request.form["height"])
            unit = request.form["unit"]

            if unit == "cm":
                height = height / 100

            bmi = weight / (height ** 2)
            result = round(bmi, 2)

            if bmi < 18.5:
                category = "Underweight"
                suggestion = "You may need to gain weight. Consider a balanced, calorie-rich diet and consult a healthcare professional."
            elif 18.5 <= bmi < 24.9:
                category = "Normal"
                suggestion = "You are in a healthy range. Maintain a balanced diet and regular physical activity."
            elif 25 <= bmi < 29.9:
                category = "Overweight"
                suggestion = "Consider a healthier lifestyle with regular exercise and a nutritious diet."
            else:
                category = "Obese"
                suggestion = "It's important to take action. Please consult a doctor or dietitian for a safe weight loss plan."

        except Exception as e:
            result = None
            category = f"Error: {e}"

    return render_template("bmi_calculator.html", result=result, category=category, suggestion=suggestion, age=age)

# ---------------- Tip Calculator ----------------
@app.route('/tip-calculator', methods=['GET', 'POST'])
def tip_calculator():
    tip = None
    if request.method == 'POST':
        bill = float(request.form['bill'])
        percent = float(request.form['percent'])
        tip = round((bill * percent) / 100, 2)
    return render_template('tip_calculator.html', tip=tip)


# ---------------- Loan Calculator ----------------
@app.route('/loan-calculator', methods=['GET', 'POST'])
def loan_calculator():
    emi = None
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate']) / (12 * 100)
        term = int(request.form['term'])
        emi = round((principal * rate * ((1 + rate) ** term)) / (((1 + rate) ** term) - 1), 2)
    return render_template('loan_calculator.html', emi=emi)


# ---------------- Unit Converter ----------------
@app.route('/unit-converter', methods=['GET', 'POST'])
def unit_converter():
    result = None
    if request.method == 'POST':
        value = float(request.form['value'])
        unit = request.form['unit']
        if unit == 'km_to_miles':
            result = round(value * 0.621371, 2)
        elif unit == 'c_to_f':
            result = round((value * 9/5) + 32, 2)
        elif unit == 'kg_to_lb':
            result = round(value * 2.20462, 2)
    return render_template('unit_converter.html', result=result)


# ---------------- Age Calculator ----------------
@app.route('/age-calculator', methods=['GET', 'POST'])
def age_calculator():
    age = None
    if request.method == 'POST':
        dob = datetime.strptime(request.form['dob'], "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return render_template('age_calculator.html', age=age)


# ---------------- Currency Converter ----------------
@app.route('/currency-converter')
def currency_converter():
    return render_template('currency_converter.html')

API_KEY = '28f16494a4a4e66dc6cc10d2'  # Your API key
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair'

@app.route('/api/convert', methods=['GET'])
def currency_api():
    amount = request.args.get('amount', type=float)
    from_currency = request.args.get('from', type=str)
    to_currency = request.args.get('to', type=str)

    if amount is None or from_currency is None or to_currency is None:
        return jsonify({'error': 'Missing parameters'}), 400
    if amount < 0:
        return jsonify({'error': 'Amount must be non-negative'}), 400

    try:
        url = f'{BASE_URL}/{from_currency}/{to_currency}'
        response = requests.get(url)
        data = response.json()

        if data.get('result') != 'success':
            return jsonify({'error': 'API error or unsupported currency'}), 400

        rate = data['conversion_rate']
        converted = round(amount * rate, 2)

        return jsonify({
            'amount': amount,
            'from': from_currency,
            'to': to_currency,
            'converted': converted
        })

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500


# ---------------- Percentage Calculator ----------------
@app.route('/percentage-calculator', methods=['GET', 'POST'])
def percentage_calculator():
    result = None
    if request.method == 'POST':
        total = float(request.form['total'])
        value = float(request.form['value'])
        if total > 0:
            result = round((value / total) * 100, 2)
    return render_template('percentage_calculator.html', result=result)


# ---------------- Discount Calculator ----------------
@app.route('/discount-calculator', methods=['GET', 'POST'])
def discount_calculator():
    result = None
    discount_amount = None
    if request.method == 'POST':
        try:
            original_price = float(request.form['original_price'])
            discount_percent = float(request.form['discount_percent'])

            discount_amount = round(original_price * (discount_percent / 100), 2)
            result = round(original_price - discount_amount, 2)
        except:
            result = "Invalid input"

    return render_template('discount_calculator.html', result=result, discount_amount=discount_amount)

#------------scientific cslculator-----------

@app.route('/scientific-calculator')
def scientific_calculator():
    return render_template('scientific_calculator.html')

#------------profit-loss calculator

@app.route("/profit-loss-calculator", methods=["GET", "POST"])
def profit_loss_calculator():
    result = None
    if request.method == "POST":
        try:
            cost_price = float(request.form["cost_price"])
            selling_price = float(request.form["selling_price"])

            if selling_price > cost_price:
                profit = selling_price - cost_price
                percent = (profit / cost_price) * 100
                result = f"Profit: ₹{profit:.2f} ({percent:.2f}%)"
            elif selling_price < cost_price:
                loss = cost_price - selling_price
                percent = (loss / cost_price) * 100
                result = f"Loss: ₹{loss:.2f} ({percent:.2f}%)"
            else:
                result = "No Profit, No Loss."
        except:
            result = "Invalid input."
    return render_template("profit_loss_calculator.html", result=result)


#---------date difference calculator-------------


@app.route('/date-difference-calculator', methods=['GET', 'POST'])
def date_difference():
    result = None
    if request.method == 'POST':
        date1_str = request.form['date1']
        date2_str = request.form['date2']
        try:
            date1 = datetime.strptime(date1_str, "%Y-%m-%d")
            date2 = datetime.strptime(date2_str, "%Y-%m-%d")

            if date2 < date1:
                date1, date2 = date2, date1  # Ensure order for positive difference

            delta = date2 - date1
            days = delta.days
            years = days // 365
            months = (days % 365) // 30

            result = f"Difference is {years} years, {months} months, and {days} days."
        except ValueError:
            result = "❌ Please enter valid dates in YYYY-MM-DD format."

    return render_template("date_difference_calculator.html", result=result)

#------gst calculator----

@app.route("/gst-calculator", methods=["GET", "POST"])
def gst_calculator():
    gst_amount = None
    total_amount = None

    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            gst_rate = float(request.form["gst_rate"])
            gst_amount = round((amount * gst_rate) / 100, 2)
            total_amount = round(amount + gst_amount, 2)
        except ValueError:
            gst_amount = total_amount = "Invalid input"

    return render_template("gst_calculator.html", gst_amount=gst_amount, total_amount=total_amount)



# ---------------- Run the App ----------------
if __name__ == '__main__':
    app.run(debug=True)
