from flask import Flask, render_template, request
import os 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    span = float(request.form['span'])
    chord = float(request.form['chord'])
    weight = float(request.form['weight'])
    density = float(request.form['density'])
    cl = float(request.form['cl'])

    area = span * chord

    speeds = list(range(10, 101, 5))
    lifts = []

    for v in speeds:
        lift = 0.5 * density * (v ** 2) * area * cl
        lifts.append(round(lift, 2))

    safe_speed = None
    for i in range(len(speeds)):
        if lifts[i] >= weight:
            safe_speed = speeds[i]
            break

    if safe_speed:
        verdict = "SAFE DESIGN: This aircraft can successfully take off."
        status = "safe"
    else:
        verdict = "UNSAFE DESIGN: This aircraft will stall."
        status = "unsafe"

    return render_template(
        'result.html',
        area=round(area, 2),
        speeds=speeds,
        lifts=lifts,
        weight=weight,
        safe_speed=safe_speed,
        verdict=verdict,
        status=status
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
