from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<title>BUBT SGPA Calculator</title>
<style>
    body {
        background: #f7f9fa;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 600px;
        margin: 40px auto;
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        padding: 30px 40px 40px 40px;
    }
    h2 {
        text-align: center;
        color: #2d6cdf;
        margin-bottom: 20px;
    }
    form {
        margin-bottom: 20px;
    }
    input[type="number"], input[type="text"] {
        padding: 6px 10px;
        border: 1px solid #bfc9d1;
        border-radius: 5px;
        width: 90%;
        margin-bottom: 8px;
        font-size: 1em;
    }
    input[type="submit"] {
        background: #2d6cdf;
        color: #fff;
        border: none;
        border-radius: 5px;
        padding: 8px 18px;
        font-size: 1em;
        cursor: pointer;
        transition: background 0.2s;
    }
    input[type="submit"]:hover {
        background: #174a8c;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        margin-bottom: 15px;
        background: #f5f8fb;
        border-radius: 8px;
        overflow: hidden;
    }
    th, td {
        padding: 10px 8px;
        text-align: center;
    }
    th {
        background: #e3eaf6;
        color: #2d6cdf;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background: #f0f4fa;
    }
    h3 {
        color: #1b4b91;
        text-align: center;
        margin-top: 25px;
    }
</style>
<div class="container">
<h2>BUBT SGPA Calculator</h2>
<form method="post">
    Number of Subjects: <input type="number" name="num_subjects" min="1" value="{{ num_subjects or 1 }}">
    <input type="submit" value="Set Subjects">
</form>
{% if num_subjects %}
    <form method="post">
        <input type="hidden" name="num_subjects" value="{{ num_subjects }}">
        <table border="1" cellpadding="5">
            <tr><th>Subject Name</th><th>Credit</th><th>Score</th></tr>
            {% for i in range(num_subjects) %}
            <tr>
                <td><input name="subject_name_{{i}}" required></td>
                <td><input name="subject_credit_{{i}}" type="number" step="0.01" min="0" required></td>
                <td><input name="subject_score_{{i}}" type="number" min="0" max="100" required></td>
            </tr>
            {% endfor %}
        </table>
        <input type="submit" value="Calculate SGPA">
    </form>
{% endif %}
{% if sgpa is not none %}
    <h3>SGPA: {{ sgpa }}</h3>
    <table border="1" cellpadding="5">
        <tr><th>Subject</th><th>Credit</th><th>Grade</th><th>Grade Point</th></tr>
        {% for s in results %}
            <tr>
                <td>{{ s['name'] }}</td>
                <td>{{ s['credit'] }}</td>
                <td>{{ s['grade'] }}</td>
                <td>{{ s['grade_point'] }}</td>
            </tr>
        {% endfor %}
    </table>
{% endif %}
</div>
"""

def get_grade(score):
    if score >= 80:
        return 'A+', 4.00
    elif score >= 75:
        return 'A', 3.75
    elif score >= 70:
        return 'A-', 3.50
    elif score >= 65:
        return 'B+', 3.25
    elif score >= 60:
        return 'B', 3.00
    elif score >= 55:
        return 'B-', 2.75
    elif score >= 50:
        return 'C+', 2.50
    elif score >= 45:
        return 'C', 2.25
    elif score >= 40:
        return 'D', 2.00
    else:
        return 'F', 0.00

@app.route("/", methods=["GET", "POST"])
def index():
    num_subjects = None
    sgpa = None
    results = []
    if request.method == "POST":
        if "num_subjects" in request.form and not request.form.get("subject_name_0"):
            try:
                num_subjects = int(request.form["num_subjects"])
            except:
                num_subjects = 1
        else:
            num_subjects = int(request.form["num_subjects"])
            total_credits = 0
            total_weighted_points = 0
            for i in range(num_subjects):
                name = request.form[f"subject_name_{i}"]
                credit = float(request.form[f"subject_credit_{i}"])
                score = int(request.form[f"subject_score_{i}"])
                grade, grade_point = get_grade(score)
                results.append({
                    'name': name,
                    'credit': credit,
                    'grade': grade,
                    'grade_point': grade_point
                })
                total_credits += credit
                total_weighted_points += grade_point * credit
            sgpa = f"{(total_weighted_points / total_credits):.2f}" if total_credits > 0 else "N/A"
    return render_template_string(HTML_FORM, num_subjects=num_subjects, sgpa=sgpa, results=results)

if __name__ == "__main__":
    app.run(debug=True)