import pandas as pd
import numpy as np


def prepare_data_2011(online_trans_cleaned):
    data_2011 = online_trans_cleaned[
        (online_trans_cleaned['invoice_date'].dt.year == 2011) &
        (online_trans_cleaned['total_order_value'] > 0)
        ]
    return data_2011


def group_data(data_2011):
    grouped_data = data_2011.groupby(['customer_id', 'country', 'description']).agg(
        total_transactions=pd.NamedAgg(column='invoice', aggfunc='nunique'),
        unique_product_count=pd.NamedAgg(column='stock_code', aggfunc='nunique'),
        recent_purchase_date=pd.NamedAgg(column='invoice_date', aggfunc='max'),
        avg_order_value=pd.NamedAgg(column='total_order_value', aggfunc='mean')
    ).reset_index()
    agg_data = grouped_data.sort_values(by='avg_order_value', ascending=False)
    agg_data.reset_index(drop=True, inplace=True)

    return agg_data


def calculate_rfm_metrics(data):
    data_2011 = prepare_data_2011(data)
    agg_data = group_data(data_2011)
    # Calculate recency
    agg_data["recency"] = round(
        (agg_data['recent_purchase_date'].max() - agg_data['recent_purchase_date']) / np.timedelta64(1, 'D'), 0)

    # Calculate frequency
    frequency_data = agg_data.groupby('customer_id')['total_transactions'].count().reset_index()
    frequency_data.rename(columns={'total_transactions': 'frequency'}, inplace=True)
    agg_data = agg_data.merge(frequency_data, on='customer_id', how='left')

    # Calculate monetary
    monetary_data = agg_data.groupby('customer_id')['avg_order_value'].sum().reset_index()
    monetary_data.rename(columns={'avg_order_value': 'monetary'}, inplace=True)
    agg_data = agg_data.merge(monetary_data, on='customer_id', how='left')

    rfm = agg_data[['customer_id', 'recency', 'frequency', 'monetary']]

    return rfm


def calculate_rfm_scores(rfm):
    rfm = calculate_rfm_metrics(rfm)
    # Calculate quantiles for recency, frequency, and monetary
    rfm['r_score'] = pd.qcut(rfm['recency'], 4, ['4', '3', '2', '1']).astype(int)
    rfm['f_score'] = pd.qcut(rfm['frequency'], 4, ['1', '2', '3', '4']).astype(int)
    rfm['m_score'] = pd.qcut(rfm['monetary'], 4, ['1', '2', '3', '4']).astype(int)

    # Calculate the RFM score by adding the scores for recency, frequency, and monetary
    rfm['RFM_Score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

    return rfm


def create_rfm_segments(rfm):
    rfm = calculate_rfm_scores(rfm)
    segment_labels = ['Basic_value', 'Standard_value', 'Premium_value']
    rfm['value_segment'] = pd.qcut(rfm['RFM_Score'], q=3, labels=segment_labels)

    rfm['RFM_customer_segments'] = ''
    rfm.loc[rfm['RFM_Score'] >= 9, 'RFM_customer_segments'] = 'Champions'
    rfm.loc[(rfm['RFM_Score'] >= 7) & (rfm['RFM_Score'] < 9), 'RFM_customer_segments'] = 'Loyal Customers'
    rfm.loc[(rfm['RFM_Score'] >= 5) & (rfm['RFM_Score'] < 7), 'RFM_customer_segments'] = 'Moderate Customers'
    rfm.loc[(rfm['RFM_Score'] >= 3) & (rfm['RFM_Score'] < 5), 'RFM_customer_segments'] = 'Inactive Customers'

    customer_segmentation = rfm.groupby('customer_id').agg(
        value_segment=('value_segment', 'first'),
        RFM_customer_segments=('RFM_customer_segments', 'first'),
        Rfm_Score=('RFM_Score', 'first')
    ).reset_index()

    return customer_segmentation
