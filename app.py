from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure Time
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival Time
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        Jet_Airways = IndiGo = Air_India = 0
        if airline == 'Jet Airways':
            Jet_Airways = 1
        elif airline == 'IndiGo':
            IndiGo = 1
        elif airline == 'Air India':
            Air_India = 1

        # Source
        source = request.form["Source"]
        s_Delhi = s_Kolkata = s_Mumbai = s_Chennai = 0
        if source == 'Delhi':
            s_Delhi = 1
        elif source == 'Kolkata':
            s_Kolkata = 1
        elif source == 'Mumbai':
            s_Mumbai = 1
        elif source == 'Chennai':
            s_Chennai = 1

        # Destination
        destination = request.form["Destination"]
        d_Cochin = d_Delhi = d_New_Delhi = d_Hyderabad = d_Kolkata = 0
        if destination == 'Cochin':
            d_Cochin = 1
        elif destination == 'Delhi':
            d_Delhi = 1
        elif destination == 'New_Delhi':
            d_New_Delhi = 1
        elif destination == 'Hyderabad':
            d_Hyderabad = 1
        elif destination == 'Kolkata':
            d_Kolkata = 1

        # Prediction - Modify to match the 9 features the model was trained on
        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min
        ]])

        output = round(prediction[0], 2)

        return render_template('index.html', prediction_text="Your Flight Price is Rs. {}".format(output))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
