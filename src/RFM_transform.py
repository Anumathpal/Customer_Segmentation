import pandas as pd
import numpy as np
def prepare_data_2011(online_trans_cleaned):
    data_2011= online_trans_cleaned[
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



# Calculate frequency and monetary function
def calculate_frequency_and_monetary(agg_data):
    frequency_data = agg_data.groupby('customer_id')['total_transactions'].count().reset_index()
    frequency_data.rename(columns={'total_transactions': 'frequency'}, inplace=True)
    agg_data = agg_data.merge(frequency_data, on='customer_id', how='left')

    monetary_data = agg_data.groupby('customer_id')['avg_order_value'].sum().reset_index()
    monetary_data.rename(columns={'avg_order_value': 'monetary'}, inplace=True)
    agg_data = agg_data.merge(monetary_data, on='customer_id', how='left')

    return agg_data


def calculate_rfm_metrics(data):
    data_2011= prepare_data_2011(data)
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







