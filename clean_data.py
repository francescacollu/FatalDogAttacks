import pandas as pd

def make_list_victim_info(victim_info):
    return victim_info.split(',')

def get_victim_info(victim_info):
    name = ''
    age = ''
    gender = ''
    if len(victim_info)==3:
        name = victim_info[0]
        age = victim_info[1]
        gender = victim_info[2]
    elif len(victim_info)==2:
        if victim_info[0].isdigit() or '<' in victim_info[0]:
            name = "na"
            age = victim_info[0]
            gender = victim_info[1]
        elif victim_info[1].isdigit():
            name = victim_info[0]
            age = victim_info[1]
            gender = "na"
    elif len(victim_info)==1:
        if victim_info[0].isdigit():
            name = "na"
            age = victim_info[0]
            gender = "na"
        else:
            if victim_info[0] == "Male" or victim_info[0] == "Female":
                name = "na"
                age = "na"
                gender = victim_info[0]
            else: 
                name = victim_info[0]
                age = "na"
                gender = "na"
    else:
        name = "na"
        age = "na"
        gender = "na"
    return [name, age, gender]

def create_victim_info_columns(df):
    if 'Victim' in df.columns:
        df['Victim'] = df['Victim'].apply(lambda x : make_list_victim_info(x))
    if 'VictimName' not in df.columns and 'Victim' in df.columns:
        df["VictimName"] = df["Victim"].apply(lambda x : get_victim_info(x)[0])
    if 'VictimAge' not in df.columns and 'Victim' in df.columns:
        df['VictimAge'] = df["Victim"].apply(lambda x : get_victim_info(x)[1])
    if 'VictimGender' not in df.columns and 'Victim' in df.columns:
        df['VictimGender'] = df["Victim"].apply(lambda x : get_victim_info(x)[2])

def create_dog_info_columns(df):
    df["DogBreedsList"] = df['Dog type (Number)'].apply(lambda x : x.split('(')[0].strip(' '))
    df["DogsNumber"] = df['Dog type (Number)'].apply(lambda x : x.split('(')[1].strip(') ') if '(' in x else '1')

def create_location_column(df):
    if 'Location' not in df.columns:
        df['Location'] = df['Circumstances'].apply(lambda x : x.split(' — ')[0] if ' — ' in x else 'na')

df = pd.read_csv("fatal_dog_attacks - Africa - Others.csv")
create_victim_info_columns(df)
create_dog_info_columns(df)
create_location_column(df)
df['Region/Country'] = "Africa"
df.to_csv("fatal_dog_attacks_Africa-Others.csv")
