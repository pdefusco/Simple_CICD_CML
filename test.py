import pandas as pd
import datetime

#pd.read_csv('data/historical.csv')['offer'].unique()


import boto3 

def get_models():
  ## Get S3 bucket
  s3 = boto3.resource('s3')
  my_bucket = s3.Bucket('demo-aws-1')  
  models = []
  ## Pull models list
  for object_summary in my_bucket.objects.filter(Prefix="datalake/pdefusco/simple_cicd_models/"):
    models.append(object_summary.key.split('/')[3])
  models = list(dict.fromkeys(models))
  
  return models
    
def find_latest(models):
  ## Get latest models
  times = list(dict.fromkeys([datetime.datetime.strptime(i[-14:],"%d%m%Y%H%M%S") for i in models]))
  latest = min(times).strftime("%d%m%Y%H%M%S")
  filtered = [model for model in models if latest in model]
  
  return filtered
  
def load_latest_pipeline(filtered):
  ## Get url for latest pipeline
  latest_pipeline_url = [model for model in find_latest(models) if "pipeline" in model][0]
  
  return latest_pipeline_url

def load_latest_lr(filtered):
  ## Get url for latest bestLR
  latest_bestLR_url = [model for model in find_latest(models) if "bestLR" in model][0]
  
  return latest_bestLR_url