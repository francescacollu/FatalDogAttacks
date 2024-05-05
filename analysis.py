import pandas as pd
import re
from breed_to_type import *

def get_most_dangerous_breed(df):
    df = df[['FatalityId','DogBreedsList']]
    df.drop_duplicates(inplace=True)
    return df.groupby(by='DogBreedsList').size().reset_index(name='Count').sort_values(by='Count', ascending=False)

def get_most_frequent_victim_gender(df):
    data = df[['FatalityId', 'VictimName', 'VictimAge', 'VictimGender']]
    data.drop_duplicates(inplace=True)
    data['VictimGender'] = df['VictimGender'].apply(lambda x : x.split(','))
    data = data.explode('VictimGender')
    data['VictimGender'] = data['VictimGender'].apply(lambda x : x.strip())
    return data.groupby(by='VictimGender').size().reset_index(name='Count').sort_values(by='Count', ascending=False)

def create_age_category(df):
    df["AgeGroup"] = pd.cut(x=df['VictimAge'], bins=[0,1,13,19,29,49,64,100], labels=["Infant (0-1)", "Child (2-13)", "Teen (14-19)", "Young Adult (20-29)", "Adult (30-49)", "Middle-Aged (50-64)", "Senior (65+)"])
    return df

def get_most_frequent_victim_age(df):
    return df.groupby(by=['AgeGroup','VictimGender']).size().reset_index(name='Count').sort_values(by='Count', ascending=False)

def summarize_cause(circumstances):
    circumstances = circumstances.lower()
    if re.search(r'head injury|head trauma|skull fracture|head', circumstances):
        return 'Blunt Force Head Trauma'
    elif re.search(r'decapitation|headless', circumstances):
        return 'Decapitation'
    elif re.search(r'blood loss|exsanguination', circumstances):
        return 'Blood Loss'
    elif re.search(r'heart attack|heart pain', circumstances):
        return 'Heart Attack'
    elif re.search(r'rabies|infected|capnocytophaga canimorsus|sepsis', circumstances):
        return 'Infections'
    elif re.search(r'neck|throat|broken neck', circumstances):
        return 'Broken Neck'
    elif re.search(r'suffocation|asphyxiation|strangulation|drowned', circumstances):
        return 'Asphyxiation'
    elif re.search(r'bites|bite|bitten', circumstances):
        return 'Generic Bite Injuries'
    else:
        return 'Unrecognized'

def deduct_cause_of_death(df):
    df['CauseOfDeath'] = df['Circumstances'].apply(summarize_cause)
    return df

def map_dog_type(df):
    df['DogType'] = df['DogBreedsList'].map(breed_to_type)
    return df

def get_most_dangerous_types(df):
    df = map_dog_type(df)
    df = df[['FatalityId','DogType']]
    df.drop_duplicates(inplace=True)
    return df.groupby(by='DogType').size().reset_index(name='Count').sort_values(by='Count', ascending=False)

###
df = pd.read_csv("fatal_dog_attacks_cleaned.csv")
df.Date = pd.to_datetime(df.Date)
df['Year'] = df.Date.dt.year
df = df[df.Year > 1999]
#df = map_dog_type(df)