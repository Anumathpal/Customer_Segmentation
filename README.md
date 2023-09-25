## Introduction to Project: Customer Segmentations

Customer segmentation is the process of dividing customers into groups based on
common characteristics so that companies can target to each group effectively and appropriately.
It is an important tool for bussiness to identify their most valuable customers and develop targeted
marketing campaigns to increase sales and customer loyalty.

### Project Overview
- This project is built upon a preprocessed dataset that has undergone thorough transformations, 
cleaning, including the resolution of missing or inconsistent data,
and the elimination of duplicates during the ETL- Pipeline projects.
- This project involves the analysis and segmentation of customer data to gain
 valuable insights into customer behaviour and characteristics. The project can 
 be broken into the following steps:

1. ``Data Extraction and Exploration``: The project begins with extracting around 400,000 records from a Redshift database,
followed by a rigorous exploration and cleaning phase. This process involves addressing 
missing values, outliers, and duplicates to ensure data quality.
2. ``Analysis and Visualization`` : To uncover patterns, trends, and insights, the data is
subjected to various analyses and visualizations. These techniques provide a clear understanding
of customer behavior.
3. ``RFM Analysis``: The project delves into RFM analysis by calculating recency, frequency, 
and monetary metrics. This step aids in evaluating customer behavior more comprehensively..
4. ``Quantile Analysis``: Following RFM analysis, a quantile analysis is performed. 
It involves creating four bins for recency, frequency, and monetary values. Each customer's
RFM score is calculated by summing their individual r_score, f_score, and m_score.
5. ``Value Segmentation`` Customers are segmented based on their RFM scores into three categories:
Basic (RFM score 3-6), Standard (RFM score 7-9), and Premium (RFM score 10-12).
6. ``Customer Segmentation``:A secondary segmentation category is created based on the RFM 
value segments. This category includes Champion, Loyal Customers, Moderate Customers, and 
Inactive Customers.
7. ``Aggregation``: The final dataset aggregates information on value segments, RFM scores,
and RFM segments for each customer.
8. ``Data Storage``:The resultant data is stored both locally and within a Docker container for 
further accessibility.


### Project Structure: Code Files and Jupyter Notebook:

- ``notebook/customer_segmention_Analyze_Viz_by_python.ipynb``: Notebook contain exploratory analysis and customer segmentation description generation.
- `` src/extract.py``: Contains the functions to connect to Redshift and extract the transactional data.
- ``src/RFM_transform.py``: Contains all essential functions to perform RFM analysis and customer segmentations.
- ``main.py``: Orchestrates the execution of the entire project by calling the necessary functions in the correct order.
- ``.env``:  An example file for setting environment variables.
- ``gitignore``: Specifies untracked files that Git should ignore.
- ``requirements.text``: A text document that contains all the libraries required to execute
    the code.
- ``Dockerfile``; Specifies the Docker image configuration for the Customer_Segmentation.
- ``.dockerignore``: Helps exclude specific files and directories when creating Docker images.

### Requirements
- Python 3.x
- psycopg2 package for connecting to Redshift
- boto3 package for connecting to AWS S3
- Python IDE and Command Line Interface

### Execution Instructions
1. Prerequisites: Ensure that have the necessary credentials and access to the Redshift database.
2. Environment Setup: Copy the ``.env.example`` file and rename it to ``.env.`` Open the ``.env`` file and fill in the required environment variables.
3. Install all the libraries required for execute ``main.py``

```
pip3 install -r requirements.txt
```

```
python3 main.py
```


### To execute the Customer_Segmentation by Docker:

### Requirements
- Docker Installation
- Command Line Interface

### Execution Instructions
- Verify that Docker is operational on your local machine.
- Disable the code `from dotenv import load_dotenv` and `load_dotenv()` in the ``main.py`` script.
- Create a copy of the ``.env.example`` file, naming it ``.env`` file and fill in the required environment variables. 

- Docker Build: Open a terminal or command prompt and navigate to the project's root directory.
   Execute the following command to build the Docker image:
```bash
  docker image build -t Customer_Segmentation:0.1 .
```
- Docker Run: After the Docker image is built, 
   run the following command to execute the ETL pipeline within a Docker container.
```bash
  docker run --env-file .env customer_segmentation:0.1
```




