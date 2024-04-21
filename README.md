# PlateVision Backend

This is a Flask-based RESTful API designed to power the PlateVision Android application. It provides functionalities for license plate detection, stolen vehicle checking, data scraping, and more.

## Technologies Used

- **Flask**: Flask is a micro web framework written in Python. It provides tools, libraries, and technologies to build web applications.

- **YOLOv5**: YOLO (You Only Look Once) is a state-of-the-art, real-time object detection system. YOLOv5 is an improved version of YOLO that is faster and more accurate.

- **Hugging Face API**: The Hugging Face API provides access to a wide range of pre-trained models for natural language processing (NLP) and computer vision tasks.

- **SQLite**: SQLite is a lightweight, serverless, SQL database engine. It is used in this project to store information about stolen vehicles scraped from online sources.

- **Flask SQLAlchemy**: Flask SQLAlchemy is a Flask extension that adds support for SQLAlchemy, a powerful SQL toolkit and Object-Relational Mapping (ORM) library.

## Features

### License Plate Detection

The backend utilizes the YOLOv5 model to detect license plates in images. It processes images received via HTTP POST requests, performs object detection, and returns bounding boxes with cropped images of the detected license plates.

### Stolen Vehicle Checking

PlateVision Backend checks scanned license plates against a database of stolen vehicles. It scrapes data from online sources, stores it in a SQLite database, and provides endpoints to query vehicle information based on license plate numbers.

### Data Scraping

The backend includes a web scraper that gathers information about stolen vehicles from online sources. It utilizes the BeautifulSoup library to parse HTML content and extract relevant data, which is then stored in the SQLite database.

### API Endpoints

PlateVision Backend offers several API endpoints for various functionalities, including:

- `/scrape`: Initiates the data scraping process to collect information about stolen vehicles from online sources and store it in the database.
- `/car-info/<license_plate>`: Retrieves information about a specific vehicle based on its license plate number.
- `/detect`: Performs license plate detection on images sent via HTTP POST requests.


- **License Plate Detection**: Send an HTTP POST request to the `/detect` endpoint with an image containing a license plate. The backend will return bounding boxes with cropped images of the detected license plates.

- **Stolen Vehicle Checking**: Utilize the `/car-info/<license_plate>` endpoint to check if a vehicle with a specific license plate number is reported as stolen. The backend will return information about the vehicle if it is found in the database.

- **Data Scraping**: Trigger the data scraping process by sending an HTTP GET request to the `/scrape` endpoint. The backend will scrape online sources for information about stolen vehicles and store it in the database.

## Contributing

Contributions to the PlateVision Backend are welcome! If you'd like to contribute, please fork the repository, create a new branch for your changes, and submit a pull request.


   
