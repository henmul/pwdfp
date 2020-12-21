from flask import Flask, render_template, jsonify, request
import joblib
import pandas as pd
import json
from imblearn.over_sampling import SMOTE
import pickle
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

app = Flask(__name__)

dts = datetime(2019, 12, 31)

# home route
#halaman home
@app.route('/')
def home():
    return render_template('home.html')

#halaman aboutus
@app.route('/abt', methods=['POST', 'GET'])
def aboutus():
    return render_template('abt.html')

#halaman dataset
@app.route('/database', methods=['POST', 'GET'])
def dataset():
    return render_template('dataset.html')

# #halaman visualisasi
@app.route('/visualize', methods=['POST', 'GET'])
def visual():
    return render_template('plot.html')

# #halaman gallery
@app.route('/gallery', methods=['POST', 'GET'])
def gallery():
    return render_template('photos.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

input_predict = pd.read_excel('aa.xlsx')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        input = request.form
        Timesbooked = int(input['Timesbooked'])
        Promoused = (int(input['Promoused']))
        Date = int(input['Date'])

        input_predict = pd.DataFrame({
            'Frequency' : [Timesbooked],
            'Score' : [Promoused],
            'Recency' : [Date]
         })

        #Making new columns for R, F and M Quartile with the whole dataset
        def RScore(x,p,d):
            if x <= d[p][0.25]:
                return 4
            elif x <= d[p][0.50]:
                return 3
            elif x <= d[p][0.75]: 
                return 2
            else:
                return 1
        # Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
        def FMScore(x,p,d):
            if x <= d[p][0.25]:
                return 1
            elif x <= d[p][0.50]:
                return 2
            elif x <= d[p][0.75]: 
                return 3
            else:
                return 4

        # Define rfm_level function
        def rfm_level(rfm_segmentation_final):
            if rfm_segmentation_final['RFM_Score'] >= 9:
                return "Opulence"
            elif ((rfm_segmentation_final['RFM_Score'] >= 8) and (rfm_segmentation_final['RFM_Score'] < 9)):
                return 'Champions'
            elif ((rfm_segmentation_final['RFM_Score'] >= 7) and (rfm_segmentation_final['RFM_Score'] < 8)):
                return 'Loyal'
            elif ((rfm_segmentation_final['RFM_Score'] >= 6) and (rfm_segmentation_final['RFM_Score'] < 7)):
                return 'Potential'
            elif ((rfm_segmentation_final['RFM_Score'] >= 5) and (rfm_segmentation_final['RFM_Score'] < 6)):
                return 'Promising'
            elif ((rfm_segmentation_final['RFM_Score'] >= 4) and (rfm_segmentation_final['RFM_Score'] < 5)):
                return 'Needs Attention'
            else:
                return 'Require Activation'

        quantiles = pd.read_excel('aa.xlsx')
        quantiles1 = quantiles.quantile(q=[0.25,0.5,0.75])

        rfm_df = input_predict

        rfm_df['R_Quartile'] = rfm_df['Recency'].apply(RScore, args=('Recency',quantiles1,))
        rfm_df['F_Quartile'] = rfm_df['Frequency'].apply(FMScore, args=('Frequency',quantiles1,))
        rfm_df['M_Quartile'] = rfm_df['Score'].apply(FMScore, args=('Score',quantiles1,))


        rfm_segmentation_final = rfm_df

        #Creating RFM segmentation table

        rfm_segmentation_final['RFMScore'] = rfm_segmentation_final.R_Quartile.map(str) \
                                    + rfm_segmentation_final.F_Quartile.map(str) \
                                    + rfm_segmentation_final.M_Quartile.map(str)

        rfm_segmentation_final['RFM_Score'] = rfm_segmentation_final['R_Quartile'] + rfm_segmentation_final['F_Quartile'] + rfm_segmentation_final['M_Quartile']

        # Create a new variable RFM_Level
        rfm_segmentation_final['RFM_Level'] = rfm_segmentation_final.apply(rfm_level, axis=1)

        # rfm_segmentation_final['RFM_Level'] = rfm_segmentation_final.apply(rfm_level)

        # # Create a new variable RFM_Level

        RFMS = rfm_segmentation_final['RFM_Score']
        RFMS = RFMS[0]         
        RFML = rfm_segmentation_final['RFM_Level']
        RFML = RFML[0]     



    return render_template('result.html', Timesbooked = Timesbooked, Promoused = Promoused, Date = Date,
                               RFMScore = RFMS, RFMLevel = RFML)



if __name__ == '__main__':
    app.run(debug=True)

