# HealthNav
HealthNav is a project aimed to increase the accessibility of healthcare facilities in Ontario.

As a part of the Ontario Engineering Competition 2023, we were instructed to create a program that serves as an interactive map to locate the optimal facility for a user based on their needs and background. This had to be done by extracting facility information from a CSV file, ranking these facilities, and then displaying the results on a map

To accomplish these requirements, we extracted information from the given CSV file. We then used Spacy to rank the facilities based on user input. How Spacy worked with our ranking system was that based on the user's condition, it would provide a similarity index to a reference word, which represented certain facilities based on their services offered or their target demographic. We then used Folium and PyQt to create a GUI and the map, which displayed the facility locations by longitude and lattitude coordinates.

Overall, our program worked to a certain degree, as using Spacy which is a type of NLP model wasn't very accurate. It produced expected results, however, it wasn't consistent. Furthermore, with the time constraint given for the competition, we weren't able to integrate the rankings with the user interface. 

However, I plan to work on this project further by potentially using a different ranking system and fully integrating the rankings with the user interface
