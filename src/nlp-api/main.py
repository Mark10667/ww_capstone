from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from routers.healthcheck import router
import torch
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import pandas as pd 
from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np
import editdistance
from google.cloud import storage
import os
import time
class Text(BaseModel):
    text: str

app = FastAPI()

@app.on_event("startup")
def setup():
   app.include_router(router)

### You shouldn't need to edit the above (except for adding imports, of course)!

#Load embedding data from GCS bucket
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"
storage_client = storage.Client("ww-columbia-capstone-student")
bucket = storage_client.bucket("voice-tracking-poc")
blob = bucket.blob("raw_data/embedding_numpy_portion_point_200k.pkl")
blob.download_to_filename('embedding_numpy_portion_point_200k.pkl')

#Load huggingface Food-Based-BERT
torch_device = 0 if torch.cuda.is_available() else -1
tokenizer = AutoTokenizer.from_pretrained("davanstrien/deberta-v3-base_fine_tuned_food_ner", model_max_length=512)
model = AutoModelForTokenClassification.from_pretrained("davanstrien/deberta-v3-base_fine_tuned_food_ner")
recognizer = pipeline("ner", model=model, tokenizer=tokenizer, device=torch_device)

#Load FAISS ANN index
df = pd.read_pickle("embedding_numpy_portion_point_200k.pkl")
embeddings = np.stack(df.embeddings)
dim = 384
param = 'Flat'
measure = faiss.METRIC_INNER_PRODUCT
index = faiss.index_factory(dim, param, measure)
index.add(embeddings)

#Load Sentence BERT
model_Sbert = SentenceTransformer('all-MiniLM-L6-v2')

def food_detection(sentence):
    #torch_device = 0 if torch.cuda.is_available() else -1
    #tokenizer = AutoTokenizer.from_pretrained("davanstrien/deberta-v3-base_fine_tuned_food_ner", model_max_length=512)
    #model = AutoModelForTokenClassification.from_pretrained("davanstrien/deberta-v3-base_fine_tuned_food_ner")
    #recognizer = pipeline("ner", model=model, tokenizer=tokenizer, device=torch_device)
    result = recognizer(sentence)
    i=0
    lst = []
    temp = ""
    while i < len(result):
        if result[i]['entity'] == 'U-FOOD':
            temp += result[i]['word'].replace('▁','')
            lst += [temp.strip()]
            temp = ''
        elif result[i]['entity'] == 'B-FOOD' and (not result[i]['word'].replace('▁','') in ['and', 'with', 'of', 's']):
            temp = ''
            temp += result[i]['word'].replace('▁','')
            temp += ' '
        elif result[i]['entity'] == 'I-FOOD' and i!=0:
            if result[i]['start'] - result[i-1]['end'] < 1 and (temp != '' or (temp == '' and (not result[i]['word'].replace('▁','') in ['and', 'with', 'of', 's']))):
                temp += result[i]['word'].replace('▁','')
                temp += ' '
        elif result[i]['entity'] == 'L-FOOD' and i!=0 and temp != '':
            if result[i]['start'] - result[i-1]['end'] < 1:
                temp += result[i]['word'].replace('▁','')
                lst += [temp.strip()]
                temp = ''
        elif result[i]['entity'] in ['U-TASTE','U-PHYSICAL_QUALITY','U-PROCESS','U-COLOR']:
            temp = ''
            temp += result[i]['word'].replace('▁','')
            temp += ' '
        if temp != '' and i==len(result)-1:
          lst += [temp.strip()]
          temp = ''
        i += 1
    delete_words = ['breakfast', 'lunch', 'dinner']
    for k in delete_words:
      if k in lst:
        lst.remove(k)
    return lst

def find_matching(word, model, index):
    word_embedding = model.encode([word], convert_to_numpy=True)
    D, I = index.search(word_embedding, 15)
    return_len = min(len(D[D>0.7]), 15)
    return I[0][:return_len],D[0][:return_len]

#calculate the edit distance and sort it
def edit_cal(lst, item, s_score):
    sim_ed_d = []
    for i in range(len(lst)):
        if editdistance.eval(item, lst[i]) == 0:
            sim_ed_d += [float('inf')]
        else:
            sim_ed_d += [s_score.tolist()[i]*10/editdistance.eval(item, lst[i])]
    sorting = [(i, j) for i, j in zip(lst, sim_ed_d)]
    x_sorted = sorted(sorting, key=lambda pair: pair[1], reverse=True)
    w_sorted = [pair[0] for pair in x_sorted]
    return w_sorted

#find the point and portion options for the matched food
def point_and_portion(lst, df):
    output_dict = dict()
    count = 0
    for i in lst:
      if not (i in output_dict.keys()):
        if count<9:
          df_food = df[df['display_name']==i]
          output_dict[i] = (df_food[['points', 'serving_desc']].values.tolist())
        else:
          break
        count = count+1
    return output_dict

def write_matching(output, processed_text):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"
    storage_client = storage.Client("ww-columbia-capstone-student")
    bucket = storage_client.bucket("voice-tracking-poc")
    upload_text = []
    upload_entities = []
    upload_matchings = []
    for i in output.keys():
        upload_text.append(processed_text)
        upload_entities.append(i)
        upload_matchings.append(output[i])
    upload_df = pd.DataFrame({'text':upload_text, 'entities':upload_entities, 'matchings':upload_matchings})
    file_title = str(time.time()) + 'matching.csv'
    upload_csv = upload_df.to_csv(file_title)
    blob_up = bucket.blob("raw_data/{}".format(file_title))
    blob_up.upload_from_filename(file_title)
        

@app.post("/process-text")
def split_string(text: Text, background_tasks: BackgroundTasks):
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application_default_credentials.json"
    #storage_client = storage.Client("ww-columbia-capstone-student")
    #bucket = storage_client.bucket("voice-tracking-poc")
    #blob = bucket.blob("raw_data/embedding_numpy_portion_point_200k.pkl")
    #blob.download_to_filename('embedding_numpy_portion_point_200k.pkl')
    #model_Sbert = SentenceTransformer('all-MiniLM-L6-v2')
    #df = pd.read_pickle("embedding_numpy_portion_point_200k.pkl")
    #embeddings = np.stack(df.embeddings)
    #dim = 384
    #param = 'Flat'
    #measure = faiss.METRIC_INNER_PRODUCT
    #index = faiss.index_factory(dim, param, measure)
    #index.add(embeddings)

    processed_text=(text.text).replace('"', '').strip()
    detected = food_detection(processed_text)
    
    output = dict()
    if detected:
        for j in range(len(detected)):
            matching, s_score = find_matching(detected[j], model_Sbert, index)
            #'0.8' in the following line is a hyperparameter that can be altered 
            if (len(s_score) == 0 or s_score[0]<=0.8) and (('with' in detected[j]) or ('and' in detected[j])):
                #if there is 'and' in the word, split it and do matching again
                to_be_split = detected[j]
                l_with = to_be_split.split(' with ')
                l_and = [i.split(' and ') for i in l_with]
                l = []
                for i in l_and:
                  for item in i:
                    l.append(item)
                for k in l:
                    matching_split, s_score_split = find_matching(k, model_Sbert, index)
                    lst = df.display_name.iloc[matching_split].tolist()
                    sorted_output = edit_cal(lst, k, s_score_split)
                    output[k] = point_and_portion(sorted_output, df)
            else:     
                lst = df.display_name.iloc[matching].tolist()
                sorted_output =  edit_cal(lst, detected[j], s_score)
                output[detected[j]] = point_and_portion(sorted_output, df)
    if output:
        background_tasks.add_task(write_matching, output, processed_text)         
    return output
