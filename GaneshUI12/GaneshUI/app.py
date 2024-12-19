from flask import Flask, render_template, request
from rdflib import Graph, Namespace, URIRef
from collections import Counter

app = Flask(__name__)

# Load the OWL ontology
g = Graph()
g.parse("Statistics.ttl", format="turtle")  # Use Stat.ttl as the ontology file

# Define the namespaces
namespace = Namespace("http://www.example.org/statistics-education#")
rdfs_namespace = Namespace("http://www.w3.org/2000/01/rdf-schema#")

@app.route('/')
def index():
    classes = {}
    
    # Query for all classes
    for s, p, o in g.triples((None, rdfs_namespace['subClassOf'], None)):
        if isinstance(o, URIRef) and o.startswith(namespace):
            class_name = o.split('#')[-1]
            if class_name not in classes:
                classes[class_name] = []

            # Find subclasses
            subclass_name = s.split('#')[-1]
            if subclass_name not in classes[class_name]:  # Avoid duplicates
                classes[class_name].append(subclass_name)

    return render_template('index.html', classes=classes)

@app.route('/subclass/<subclass_name>')
def subclass(subclass_name):
    if subclass_name.lower() == "mean":
        return render_template('calculate_mean.html', subclass_name=subclass_name)
    elif subclass_name.lower() == "introductorystatistics":
        return render_template('introductory_statistics.html')  # New route for IntroductoryStatistics
    elif subclass_name.lower() == "median":
        return render_template('calculate_median.html', subclass_name=subclass_name)  # Placeholder for Median
    elif subclass_name.lower() == "mode":
        return render_template('calculate_mode.html', subclass_name=subclass_name)  # Placeholder for Mode
    else:
        return render_template('under_cons.html', subclass_name=subclass_name)  # Handle unknown subclasses

@app.route('/subclass/mean/calculate_mean', methods=['POST'])
def calculate_mean():
    numbers_input = request.form['numbers']
    numbers = [float(num.strip()) for num in numbers_input.split(',') if num.strip()]
    mean_value = sum(numbers) / len(numbers) if numbers else 0
    return render_template('calculate_mean.html', subclass_name="Mean", mean=mean_value)

@app.route('/subclass/median/calculate_median', methods=['POST'])
def calculate_median():
    numbers_input = request.form['numbers']
    numbers = sorted([float(num.strip()) for num in numbers_input.split(',') if num.strip()])
    n = len(numbers)
    if n == 0:
        median_value = 0
    elif n % 2 == 1:
        median_value = numbers[n // 2]
    else:
        median_value = (numbers[n // 2 - 1] + numbers[n // 2]) / 2
    return render_template('calculate_median.html', subclass_name="Median", median=median_value)

@app.route('/subclass/mode/calculate_mode', methods=['POST'])

def calculate_mode():
    numbers_input = request.form['numbers']
    numbers = [float(num.strip()) for num in numbers_input.split(',') if num.strip()]
    if not numbers:
        mode_value = None
    else:
        # Count the frequency of each number
        frequency = Counter(numbers)
        max_count = max(frequency.values())
        # Find all numbers that have the maximum frequency
        mode_value = [num for num, count in frequency.items() if count == max_count]
        # If all numbers are unique, there is no mode
        if len(mode_value) == len(numbers):
            mode_value = None
    return render_template('calculate_mode.html', subclass_name="Mode", mode=mode_value)



if __name__ == '__main__':
    app.run(debug=True)