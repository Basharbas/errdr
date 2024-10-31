from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>محول الأعداد</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            direction: rtl; 
            background-color: #f0f8ff; 
            color: #333; 
            margin: 0; 
            padding: 0; 
        }
        .container { 
            max-width: 600px; 
            margin: 50px auto; 
            padding: 20px; 
            background-color: #fff; 
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); 
            border-radius: 8px; 
        }
        .header {
            display: flex; 
            align-items: center; 
            justify-content: center; 
            margin-bottom: 20px; 
        }
        .header img { 
            max-width: 50px; 
            margin-left: 15px; 
        }
        input[type="text"] { 
            width: 100%; 
            padding: 10px; 
            margin: 10px 0; 
            border: 1px solid #ccc; 
            border-radius: 4px; 
        }
        input[type="submit"] { 
            padding: 10px 20px; 
            background-color: #007bff; 
            color: #fff; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            transition: background-color 0.3s; 
        }
        input[type="submit"]:hover { 
            background-color: #0056b3; 
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            margin-top: 20px; 
        }
        th, td { 
            border: 1px solid #ccc; 
            padding: 10px; 
            text-align: center; 
        }
        footer { 
            text-align: center; 
            margin-top: 20px; 
            font-size: 0.9em; 
            color: #555; 
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <img src="https://via.placeholder.com/50" alt="صورة توضيحية">
        <h2>محول الأعداد بين النظام الثنائي والنظام العشري</h2>
    </div>
    <form method="post">
        <label for="binary">أدخل عدد ثنائي:</label>
        <input type="text" name="binary" id="binary" value="{{ binary }}">

        <label for="decimal">أدخل عدد عشري:</label>
        <input type="text" name="decimal" id="decimal" value="{{ decimal }}">

        <input type="submit" name="convert" value="تحويل">
    </form>

    {% if decimal_result is not none %}
        <h3>النتيجة العشرية: {{ decimal_result }}</h3>
        <h4>خطوات التحويل:</h4>
        <table>
            <tr><th>الخطوة</th></tr>
            {% for step in binary_steps %}
                <tr><td>{{ step }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}

    {% if binary_result is not none %}
        <h3>النتيجة الثنائية: {{ binary_result }}</h3>
        <h4>خطوات التحويل:</h4>
        <table>
            <tr><th>الخطوة</th></tr>
            {% for step in decimal_steps %}
                <tr><td>{{ step }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}
</div>

<footer>
    جميع الحقوق محفوظة المبرمج بشار
</footer>

</body>
</html>
'''

def binary_to_decimal(binary):
    decimal = 0
    steps = []
    binary_reversed = binary[::-1]
    for index, bit in enumerate(binary_reversed):
        value = int(bit) * (2 ** index)
        decimal += value
        steps.append(f"({bit} * 2^{index}) = {value}")
    return decimal, steps

def decimal_to_binary(decimal):
    binary = ''
    steps = []
    decimal = int(decimal)
    while decimal > 0:
        remainder = decimal % 2
        binary = str(remainder) + binary
        steps.append(f"{decimal} / 2 = {decimal // 2} الباقي = {remainder}")
        decimal //= 2
    return binary, steps

@app.route('/', methods=['GET', 'POST'])
def index():
    binary = request.form.get('binary', '')
    decimal = request.form.get('decimal', '')
    decimal_result = None
    binary_result = None
    binary_steps = []
    decimal_steps = []

    if request.method == 'POST':
        if binary:
            decimal_result, binary_steps = binary_to_decimal(binary)
        if decimal:
            binary_result, decimal_steps = decimal_to_binary(decimal)

    return render_template_string(HTML_TEMPLATE, binary=binary, decimal=decimal,
                                  decimal_result=decimal_result, binary_result=binary_result,
                                  binary_steps=binary_steps, decimal_steps=decimal_steps)

if __name__ == '__main__':
    app.run(debug=True)