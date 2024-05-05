import pandas as pd
import os

folder = 'results'

filelist = [file for file in os.listdir(folder)]
dataset_list = []
for file in filelist:
    print(file)
    df = pd.read_csv(folder+'/'+file)
    df = df[['Date', 'VictimName', 'VictimAge', 'VictimGender', 'DogBreedsList', 'DogsNumber', 'Circumstances', 'Location', 'Region/Country']]
    dataset_list.append(df)

fatal_dog_attacks_dataset = pd.concat(dataset_list)
fatal_dog_attacks_dataset.to_csv("results/global_fatal_dog_attacks.csv")