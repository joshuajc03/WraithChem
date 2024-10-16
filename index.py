from flask import Flask, render_template, request
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder="templates")
CORS(app)

# Function to fetch data from PubChem database
def fetch_compound_info(compound_name):
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    url = f"{base_url}/compound/name/{compound_name}/property/MolecularFormula,MolecularWeight,InChIKey,ExactMass,Charge/JSON"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        compound_info = data["PropertyTable"]["Properties"][0]
        return {
            "name": compound_name.capitalize(),
            "formula": compound_info.get("MolecularFormula"),
            "weight": compound_info.get("MolecularWeight"),
            "exact_mass": compound_info.get("ExactMass"),
            "charge": compound_info.get("Charge"),
            "inchikey": compound_info.get("InChIKey"),
        }
    except Exception as err:
        return {"error": str(err)}

# Define the main route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        compound_name = request.form["compound_name"]
        compound_info = fetch_compound_info(compound_name)
        return render_template("index.html", compound_info=compound_info)
    return render_template("index.html", compound_info=None)



if __name__ == "__main__":
    app.run(debug=True)
