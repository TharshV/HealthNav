import csv
import sys
import io
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)
        # Layout
        form_layout = QFormLayout()
        # Input fields
        self.symptoms_input = QLineEdit()
        form_layout.addRow("Symptoms:", self.symptoms_input)
        self.health_conditions_input = QLineEdit()
        form_layout.addRow("Health Conditions:", self.health_conditions_input)
        self.location_input = QLineEdit()
        form_layout.addRow("Location:", self.location_input)
        self.age_input = QLineEdit()
        form_layout.addRow("Age:", self.age_input)
        self.sex_input = QLineEdit()
        form_layout.addRow("Sex:", self.sex_input)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.on_submit)
        form_layout.addRow(submit_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        self.webView = QWebEngineView()
        main_layout.addWidget(self.webView)
        self.setLayout(main_layout)

    def on_submit(self):
        try:
            with open("readingFile.csv") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                locations = []
                for row in csv_reader:
                    latitude = float(row["latitude"])
                    longitude = float(row["longitude"])
                    location_name = row["facilityname"]
                    contact = row["contact"]
                    locations.append((latitude, longitude, location_name, contact))
        except ValueError:
            print("Invalid coordinates, please check your csv file.")
            return

        # Create a map centered on the first location
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=13,
            location=[locations[0][0], locations[0][1]]
        )

        # Add a marker for each location with contact info in the popup
        for latitude, longitude, location_name, contact in locations:
            folium.Marker(location=[latitude, longitude], popup=location_name + "<br>" + contact).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        
         #get the user inputs
        symptoms = self.symptoms_input.text()
        health_conditions = self.health_conditions_input.text()
        location = self.location_input.text()
        age = self.age_input.text()
        sex = self.sex_input.text()
        
        #write the user inputs to a new csv file
        with open('user_data.csv', mode='w') as user_data:
            fieldnames = ['symptoms', 'health_conditions', 'location', 'age', 'sex']
            writer = csv.DictWriter(user_data, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'symptoms': symptoms, 'health_conditions': health_conditions, 'location': location, 'age': age, 'sex': sex})

        self.webView.setHtml(data.getvalue().decode())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    myApp = MyApp()
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')