#Selecting the known Treshold
import pandas as pd

Timesbooked = int(1)

Promoused = int(1)

Date = int(250)


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

print(RFMS)