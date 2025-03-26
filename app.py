from flask import Flask, render_template, request
from singly_beam_design import singly_beam_design
from doubly_beam_design import doubly_beam_design
from continuous_beam_design import continuous_beam_design
from cantilever_beam_design import cantilever_beam_design

app = Flask(__name__)

# Define the model path globally to avoid passing it repeatedly
MODEL_PATH = "C:/Users/arjun/Desktop/BeamDesignApp/singly_beam_model.pkl"
MODEL_PATH_classification = "C:/Users/arjun/Desktop/BeamDesignApp/classification_model.pkl"
MODEL_PATH_regression = "C:/Users/arjun/Desktop/BeamDesignApp/regression_model.pkl"
MODEL_PATH_classification_co = "C:/Users/arjun/Desktop/BeamDesignApp/classification_model_co.pkl"
MODEL_PATH_regression_0_co = "C:/Users/arjun/Desktop/BeamDesignApp/regression_model_0_co.pkl"
MODEL_PATH_regression_1_co = "C:/Users/arjun/Desktop/BeamDesignApp/regression_model_1_co.pkl"
MODEL_PATH_classification_ca = "C:/Users/arjun/Desktop/BeamDesignApp/classification_model_ca.pkl"
MODEL_PATH_regression_0_ca = "C:/Users/arjun/Desktop/BeamDesignApp/regression_model_0_ca.pkl"
MODEL_PATH_regression_1_ca = "C:/Users/arjun/Desktop/BeamDesignApp/regression_model_1_ca.pkl"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/beam-input/<beam_type>')
def beam_input(beam_type):
    # Choose the correct template based on beam type
    if beam_type == "singly":
        template = 'beam_input_singly.html'
    elif beam_type == "doubly":
        template = 'beam_input_doubly.html'
    elif beam_type == "cantilever":
        template = 'beam_input_cantilever.html'
    elif beam_type == "continuous":
        template = 'beam_input_continuous.html'
    else:
        # Return an error page or a 404 if an invalid beam type is provided
        return "Beam type not recognized", 404
    return render_template(template, beam_type=beam_type)

@app.route('/design', methods=['POST'])
def design():
    # Get the beam type from the form
    beam_type = request.form['beam_type']

    # Collect form data
    clear_span = float(request.form['clear_span'])
    live_load = float(request.form['live_load'])
    support_width = float(request.form['support_width'])
    steel_grade = int(request.form['steel_grade'])
    concrete_grade = int(request.form['concrete_grade'])

    # Process design data based on the beam type
    if beam_type == "singly":
        design_data = singly_beam_design(clear_span, live_load, concrete_grade, steel_grade, support_width, MODEL_PATH)
        template = 'result_singly.html'
        # Render the corresponding template with design data
        return render_template(
            template,
            summary=design_data["design_summary"],
            results=design_data["results"],
            error=design_data.get("error", False)
        )
    elif beam_type == "doubly":
        design_data = doubly_beam_design(clear_span, live_load, concrete_grade, steel_grade, support_width, MODEL_PATH_classification, MODEL_PATH_regression)
        template = 'result_doubly.html'
        # Render the corresponding template with design data
        return render_template(
            template,
            summary=design_data["design_summary"],
            results=design_data["results"],
            error=design_data.get("error", False)
        )
    elif beam_type == "cantilever":
        design_data = cantilever_beam_design(clear_span, live_load, concrete_grade, steel_grade, support_width,  MODEL_PATH_classification_ca, MODEL_PATH_regression_0_ca, MODEL_PATH_regression_1_ca)
        template = 'result_cantilever.html'
        # Render the corresponding template with design data
        return render_template(
            template,
            summary=design_data["design_summary"],
            results=design_data["results"],
            mode=design_data["results"]["mode"],
            error=design_data.get("error", False)
        )
    elif beam_type == "continuous":
        dead_load = float(request.form['dead_load'])
        design_data = continuous_beam_design(clear_span, live_load, dead_load, concrete_grade, steel_grade, support_width, MODEL_PATH_classification_co, MODEL_PATH_regression_0_co, MODEL_PATH_regression_1_co)
        template = 'result_continuous.html'
        # Render the corresponding template with design data
        return render_template(
            template,
            summary=design_data["design_summary"],
            results=design_data["results"],
            mode=design_data["results"]["mode"],
            error=design_data.get("error", False)
        )
    else:
        return "Beam type not recognized", 404

@app.route('/generate-image')
def generate_image():
    # Retrieve parameters from the query string
    breadth = request.args.get('breadth', type=int)
    depth = request.args.get('depth', type=int)
    no_of_bars = request.args.get('no_of_bars', type=int)
    dia_of_bar = request.args.get('dia_of_bar', type=int)
    
    # Render `generate_image.html` with these parameters
    return render_template(
        'generate_image.html',
        breadth=breadth,
        depth=depth,
        no_of_bars=no_of_bars,
        dia_of_bar=dia_of_bar
    )

@app.route('/generate-image_doubly')
def generate_image_doubly():
    # Retrieve parameters from the query string
    breadth = request.args.get('breadth', type=int)
    depth = request.args.get('depth', type=int)
    no_of_bar_tens = request.args.get('no_of_bar_tens', type=int)
    bar_dia_tens = request.args.get('bar_dia_tens', type=int)
    
    # Render `generate_image_doubly.html` with these parameters
    return render_template(
        'generate_image_doubly.html',
        breadth=breadth,
        depth=depth,
        no_of_bar_tens=no_of_bar_tens,
        bar_dia_tens=bar_dia_tens
    )

@app.route('/generate-image_cantilever_s')
def generate_image_cantilever_s():
    # Retrieve parameters from the query string
    breadth = request.args.get('breadth', type=int)
    depth = request.args.get('depth', type=int)
    no_of_bar_tens = request.args.get('no_of_bar_tens', type=int)
    bar_dia_tens = request.args.get('bar_dia_tens', type=int)
    
    # Render `generate_image_doubly.html` with these parameters
    return render_template(
        'generate_image_cantilever_s.html',
        breadth=breadth,
        depth=depth,
        no_of_bar_tens=no_of_bar_tens,
        bar_dia_tens=bar_dia_tens
    )

@app.route('/generate-image_cantilever_d')
def generate_image_cantilever_d():
    # Retrieve parameters from the query string
    breadth = request.args.get('breadth', type=int)
    depth = request.args.get('depth', type=int)
    no_of_bar_tens = request.args.get('no_of_bar_tens', type=int)
    bar_dia_tens = request.args.get('bar_dia_tens', type=int)
    
    # Render `generate_image_doubly.html` with these parameters
    return render_template(
        'generate_image_cantilever_d.html',
        breadth=breadth,
        depth=depth,
        no_of_bar_tens=no_of_bar_tens,
        bar_dia_tens=bar_dia_tens
    )

@app.route('/generate-image_continuous_supp')
def generate_image_continuous_supp():
    # Retrieve parameters from the query string
    b = request.args.get('b', type=int)
    d = request.args.get('d', type=int)
    no_of_bar_tens_supp = request.args.get('no_of_bar_tens_supp', type=int)
    dia_bar_tens_supp = request.args.get('dia_bar_tens_supp', type=int)
    no_of_bar_comp_supp = request.args.get('no_of_bar_comp_supp', type=int)
    dia_bar_comp_supp = request.args.get('dia_bar_comp_supp', type=int)

    # Render `generate_image_continuous_supp.html` with these parameters
    return render_template(
        'generate_image_continuous_supp.html',
        b=b,
        d=d,
        no_of_bar_tens_supp=no_of_bar_tens_supp,
        dia_bar_tens_supp=dia_bar_tens_supp,
        no_of_bar_comp_supp=no_of_bar_comp_supp,
        dia_bar_comp_supp=dia_bar_comp_supp
  
    )
@app.route('/generate-image_continuous_mid')
def generate_image_continuous_mid():
    # Retrieve parameters from the query string
    b = request.args.get('b', type=int)
    d = request.args.get('d', type=int)
    no_of_bar_tens_mid = request.args.get('no_of_bar_tens_mid', type=int)
    dia_bar_tens_mid = request.args.get('dia_bar_tens_mid', type=int)
    no_of_bar_comp_mid = request.args.get('no_of_bar_comp_mid', type=int)
    dia_bar_comp_mid = request.args.get('dia_bar_comp_mid', type=int)

    # Render `generate_image_continuous_mid.html` with these parameters
    return render_template(
        'generate_image_continuous_mid.html',
        b=b,
        d=d,
        no_of_bar_tens_mid=no_of_bar_tens_mid,
        dia_bar_tens_mid=dia_bar_tens_mid,
        no_of_bar_comp_mid=no_of_bar_comp_mid,
        dia_bar_comp_mid=dia_bar_comp_mid
  
    )

if __name__ == "__main__":
    app.run(debug=True)
