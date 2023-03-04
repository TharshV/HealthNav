import csv
import spacy
from geopy.geocoders import Nominatim
import h3

# Type Ranking Algorithm
# Example command line symptom input

symptomlist = []
age = int(input("What is your age in years?:\t"))
city = input("What is your city? (City, ON):\t")
while True:
    symptom = input("What are your symptoms (no acronyms)? Please enter them in one by one or 'e' to exit:\t")
    if symptom == 'e':
        break
    symptomlist.append(symptom)

# Define comparisons

nlp = spacy.load("en_core_web_lg") # Create nlp model

types = ["General Emergency Hospital Diseases", "Clinic Urgent Quick Common Care", "Pharmacy Drug", "Special Rare"]

# Loop through comparisons
def rank(list1, list2):
    rankings = [] # a list of lists, in the form [type, similarity] (in terms of inputted symptoms)
    for i in list1:
        dynamic_sum = 0
        x = nlp(i)
        for j in list2:
            y = nlp(j)
            similarity = x.similarity(y)
            dynamic_sum += similarity
        rankings.append([i,dynamic_sum])
    return rankings

type_rankings = rank(types, symptomlist)

# sort processed NLP rankings
nlp_rankings = [x[0] for x in sorted(type_rankings, key=lambda x: x[1], reverse=True)]

# Override 

if age < 16:
    nlp_rankings.insert(0, "Pediatrics")
    nlp_rankings.append("Adult Hospital")
    nlp_rankings.append("LTC")
elif age > 55 and nlp_rankings[0] != types[0]:
    nlp_rankings.insert(0, "LTC")
    nlp_rankings.append("Adult Hospital")
    nlp_rankings.append("Pediatrics")
else:
    nlp_rankings.insert(1, "Adult Hospital")
    nlp_rankings.append("LTC")
    nlp_rankings.append("Pediatrics")

replace_list = ["Hospital", "Clinic", "Pharmacy", "Specialized Care"]

for i in range(4):
    x = nlp_rankings.index(types[i])
    nlp_rankings.pop(x)
    nlp_rankings.insert(x, replace_list[i])

# General Rankings
general_vars = ["heart, blood, heart attack, angina, cardiac", "vascular, vein, artery, lymphatic, vessel", "trauma, fall, pain, burn", "intensive care unit"]

general_rankings = rank(general_vars, symptomlist)
general_rankings = [x[0] for x in sorted(general_rankings, key=lambda x: x[1], reverse=True)]

# Grading system    
''
geolocator = Nominatim(user_agent="MyApp")
location = geolocator.geocode(city)
coords_1 = (location.latitude, location.longitude)

locations_sorted = [] 
print(nlp_rankings)
with open('readingFile.csv', 'r') as csv_file: #Parse csv files
    csv_reader = csv.reader(csv_file) #Creates a csv_reader object
    for value in nlp_rankings:
        for line in csv_reader:
            if (line[2].find(",") != -1):
                if (line[2].split(','))[0] == value or (line[2].split(','))[1] == value:
                    distance = h3.point_dist(coords_1, (float(line[3]),float(line[4])), unit='m')
                    locations_sorted.append([line[0], distance])
            elif line[2] == value:
                distance = h3.point_dist(coords_1, (float(line[3]),float(line[4])), unit='m')
                locations_sorted.append([line[0], distance])
    
    print(locations_sorted)