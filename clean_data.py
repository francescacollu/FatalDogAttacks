import math
import pandas as pd
import numpy as np

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

def clean_gender_column(df):
    return df['VictimGender'].apply(lambda x : x.strip(' ').replace('Famale', 'Female').replace('Females', 'Female').replace('Girl', 'Female') if not isinstance(x,float) else x)

def clean_age_column(df):
    df['VictimAge'] = df['VictimAge'].apply(lambda x : x.strip(' ').replace('<', '').replace('>', '').replace('years', '').replace('year', '').replace(' months', '/12').replace(' month', '/12').replace(' weeks old', '/52.1429').replace(' weeks', '/52.1429').replace(' days', '/365').replace('*Unknown*', 'na').replace('Undisclosed', 'na').replace('Unknown', 'na').replace('Unspecified, adult', 'na').replace('Child', '6').replace('Infant', '0.5').replace('Adult', '20').replace('Newborn', '0.1').replace('Elder', '70').strip('* ').split('or')[0].split('to')[0].replace('s', '') if not isinstance(x,float) else x)
    df['VictimAge'] = df['VictimAge'].apply(lambda x : x.split(','))
    df = df.explode('VictimAge')
    df.VictimAge = df.VictimAge.apply(lambda x : round(eval(x),2) if x != 'na' else x)
    df['VictimAge'].replace('na', np.nan, inplace=True)
    return df

def clean_victim_columns(df):
    df['VictimGender'] = df['VictimGender'].apply(lambda x : x.strip(' ').replace('Famale', 'Female').replace('Females', 'Female').replace('Girl', 'Female') if not isinstance(x,float) else x)
    df['VictimGender'] = df['VictimGender'].apply(lambda x : x.split(','))
    df['VictimAge'] = df['VictimAge'].apply(lambda x : x.strip(' ').replace('<', '').replace('>', '').replace('years', '').replace('year', '').replace(' months', '/12').replace(' month', '/12').replace(' weeks old', '/52.1429').replace(' weeks', '/52.1429').replace(' days', '/365').replace('*Unknown*', 'na').replace('Undisclosed', 'na').replace('Unknown', 'na').replace('Unspecified, adult', 'na').replace('Child', '6').replace('Infant', '0.5').replace('Adult', '20').replace('Newborn', '0.1').replace('Elder', '70').strip('* ').split('or')[0].split('to')[0].replace('s', '') if not isinstance(x,float) else x)
    df['VictimAge'] = df['VictimAge'].apply(lambda x : x.split(','))
    df = df.explode(['VictimAge', 'VictimGender'])
    df.VictimAge = df.VictimAge.apply(lambda x : round(eval(x),2) if x != 'na' else x)
    df['VictimAge'].replace('na', np.nan, inplace=True)
    df['VictimGender'] = df['VictimGender'].apply(lambda x : x.strip(' '))
    return df


def clean_dog_columns(df):
    df['DogBreedsList'] = df['DogBreedsList'].apply(lambda x : x.title().replace('German Shephard', 'German Shepherd').replace('German Shephed', 'German Shepherd').replace('\n', '').replace('Doberman Pinscher', 'Doberman').replace('German Shepherd and Husky cross sled dogs', 'German Shepherd, Husky Cross').replace('Alsatian', 'German Shepherd').replace('Staffordshire Bull Terriers', 'Staffordshire Bull Terrier').replace('Jack Russell Terrier Cross', 'Jack Russell Terrier').replace('Pit Bulls', 'Pit Bull').replace('Bull Dog', 'Bulldog').replace('Bulldogs', 'Bulldog').replace('Italian Mastiff', 'Cane Corso').strip(' ').replace('German Shepherds', 'German Shepherd').replace('Xcoyote Cross', 'X Coyote').replace('Unknown Number, ', '').replace('Terriers', 'Terrier').replace('Huskies', 'Husky').replace('Unidentified', 'Unknown').replace('Xgerman', 'X German').replace('Pitt Bull', 'Pit Bull').replace('Dogs','Dog').replace('Pack Of Stray Dog','Stray Dog').replace('Unknown Large Breeds','Unknown').replace('Unknown Breed','Unknown').replace('Rottweilers', 'Rottweiler').replace('Mixes', 'Mix').replace('Crosses', 'Cross').replace('Belgian Shepherd Of The Variety: Malinois', 'Belgian Shepherd - Malinois').replace('Belgian Shepherd Of The Variety Malinois', 'Belgian Shepherd - Malinois').replace('Undisclosed', 'Unknown').replace('Pit Bull Of The Variety Pit Monster', 'Pit Bull - Pit Monster').replace('Pack Of Stray Husky Cross', 'Husky Cross').replace('Husky X Wolf Crossed Sled Dog', 'Husky X Wolf Cross').replace('Mongrels', 'Mixed Breed').replace('Mutt', 'Mixed Breed').replace('German Shepherd And Husky Cross Sled Dog', 'German Shepherd, Husky Cross').replace('German Shepherd And Labrador Retriever Cross', 'German Shepherd X Labrador Retriever').replace('Husky Sled Dog', 'Husky').replace('Border Collie And Mongrel German Shepherd', 'Border Collie, German Shepherd Cross').replace('Alaskan Malamute Sled Dog', 'Alaskan Malamute').replace('Siberian Husky Sled Dog', 'Siberian Husky').replace('German Shepherd Xhusky Cross Sled Dog', 'German Shepherd X Husky Cross').replace('Mongrel', 'Mixed Breed').replace('Mixed Medium Sized Dog', 'Mixed Breed').replace('Alaskan Malamutes', 'Alaskan Malamute').replace('Unreported Large Breed', 'Unknown').replace('Rez Dog - Either A Pit Bull Mix Or Rottweiler Mix, Pending Dna Results', 'Stray Dog').replace('Rez Dog', 'Stray Dog').replace('English Bulldog', 'Bulldog').replace('Pack Of Livestock Guarding Dog', 'Unknown').replace('Pit Bull Or Rottweiler', 'Pit Bull').replace('Mastín Leonés', 'Spanish Mastiff').replace('Carea Leonés', 'Leonese Sheepdog').replace('St. Bernard', 'Saint Bernard').replace('St Bernard', 'Saint Bernard').replace('Bullmastiffs', 'Bullmastiff').replace('Stray Dog - Either A Pit Bull Mix Or Rottweiler Mix', 'Stray Dog').replace('Bulldog Type Or Aylestone Bulldog', 'Bulldog Type').replace('American Bulldogmastiff-Bull', 'American Masti-Bull').replace('Bulldog-Cross', 'Bulldog Cross').replace('Staffordshire Bull Terrier And Mastiff Cross', 'Mastiff X Staffordshire Bull Terrier').replace('American Bully Xls', 'American Bully Xl').replace('American Bully Xl Or Cane Corso', 'American Bully Xl').replace('Great Dane', 'German Mastiff').replace('Mix Breed', 'Mixed Breed').replace('Stafford Breed', 'Staffordshire Bull Terrier').replace('Stafford Cross', 'Staffordshire Bull Terrier Cross').replace('Grønlandshund', 'Greenland Dog').replace('Stray Dog', 'Unknown').replace('Mixed Breed', 'Unknown'))
    df['DogBreedsList'] = df['DogBreedsList'].str.replace(r'\[\d+\]', '', regex=True).str.replace(r'\(\d+\)', '', regex=True).str.replace(r'^Dog$', 'Unknown', regex=True).str.replace(r'^Jack Russell$', 'Jack Russell Terrier', regex=True).str.replace(r'^Pit Bull Terrier$', 'American Pit Bull Terrier', regex=True)
    df['DogBreedsList'] = df['DogBreedsList'].apply(lambda x : x.split(','))
    df['DogsNumber'] = df['DogsNumber'].apply(lambda x : x.split(','))
    df = df.explode(['DogBreedsList', 'DogsNumber'])
    df['DogBreedsList'] = df['DogBreedsList'].apply(lambda x : x.strip())
    df['DogBreedsList'] = df['DogBreedsList'].apply(lambda x : sorted(x.split(' X ')))
    df['DogBreedsList'] = df['DogBreedsList'].apply(lambda x : [y.strip() for y in x])
    df['DogBreedsList'] = df['DogBreedsList'].apply(lambda x : ' X '.join(x) if len(x)>1 else ''.join(x))
    return df

def clean_date_column(df):
    df.Date = pd.to_datetime(df.Date)
    return df

def convert_to_number(value):
    if '-' in value:
        # Split on the dash and take the midpoint
        parts = value.split('-')
        return math.ceil((float(parts[0]) + float(parts[1])) / 2)
    elif '–' in value:
        parts = value.split('–')
        return math.ceil((float(parts[0]) + float(parts[1])) / 2)
    elif 'to' in value:
        # Split on 'to' and take the midpoint
        parts = value.split('to')
        return math.ceil((float(parts[0].strip()) + float(parts[1].strip())) / 2)
    elif 'or' in value:
        # Split on 'to' and take the midpoint
        parts = value.split('or')
        return math.ceil((float(parts[0].strip()) + float(parts[1].strip())) / 2)
    elif '+' in value:
        # Remove the '+' and use the number
        return float(value.replace('+', '').strip())
    else:
        # If none of the above, just convert directly
        return float(value)

def clean_dogs_number(df):
    df['DogsNumber'] = df['DogsNumber'].apply(lambda x : x.strip(' ').replace('Unknown number', 'na').replace('large pack', '10').replace('pack', '4').replace('(1', '1').replace('1)', '1'))
    df['DogsNumber'].replace('na', np.nan, inplace=True)
    df.DogsNumber = df.DogsNumber.apply(lambda x : convert_to_number(x) if not isinstance(x,float) else x)
    return df

def add_id_column(df):
    df['FatalityId'] = range(1, len(df)+1)
    first_col = df.pop('FatalityId')
    df.insert(0, 'FatalityId', first_col)
    return df

def clean_european_country_column(df):
    data = df[df['Country-Region']=='Europe']
    data['Country-Region'] = data['Location'].apply(lambda x : x.split(',')[0])
    return data

def clean_dataset(df):
    df = clean_victim_columns(df)
    df = clean_dog_columns(df)
    df = clean_dogs_number(df)
    df = clean_date_column(df)
    return df

###
df = pd.read_csv("fatal_dog_attacks.csv")
cleaned_df = clean_dataset(df)
cleaned_df.to_csv("fatal_dog_attacks_cleaned.csv", index=False)


#df['Breeds'] = df.DogBreedsList.apply(lambda x : len(x))
#df['Number'] = df.DogsNumber.apply(lambda x : len(x))
#df[df.Breeds != df.Number]