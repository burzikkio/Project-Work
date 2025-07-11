from flask import Flask, render_template, request
import random
import math

app = Flask(__name__)

# Materiali e relativi prodotti
materials = {
    "Plexiglas": ["Pannello 10x20", "Pannello 20x40", "Disco 15cm"],
    "Gomma": ["Guarnizione tonda", "Guarnizione rettangolare", "Paracolpi"],
    "Lana vetro": ["Isolante piccolo", "Isolante medio", "Isolante grande"]
}

# Funzione per generare dati casuali di produzione con logica corretta per dimensione

def generate_production_data(selected_products):
    data = {}
    total_time = 0

    for product in selected_products:
        quantity = random.randint(50, 200)

        # Fattore dimensione: 1.0 (piccolo) fino a 3.0 (grande)
        size_factor = round(random.uniform(1.0, 3.0), 2)
        base_time = 30  # base time in minuti
        time_per_unit = int(base_time * size_factor)

        daily_capacity = 1440 // time_per_unit
        days_required = math.ceil(quantity / daily_capacity)
        product_time = days_required * daily_capacity * time_per_unit

        total_time += product_time

        data[product] = {
            "quantity": quantity,
            "size_factor": size_factor,
            "time_per_unit": time_per_unit,
            "daily_capacity": daily_capacity,
            "days_required": days_required,
            "product_time": product_time
        }

    return data, total_time

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_material = None
    selected_products = []
    results = None
    total_time = 0

    if request.method == 'POST':
        selected_material = request.form.get("material")
        selected_products = request.form.getlist("products")

        if selected_material and selected_products:
            results, total_time = generate_production_data(selected_products)

    return render_template(
        'index.html',
        materials=materials,
        selected_material=selected_material,
        selected_products=selected_products,
        results=results,
        total_time=total_time,
        company_name="Athen S.P.A."
    )

if __name__ == '__main__':
    app.run(debug=True)
