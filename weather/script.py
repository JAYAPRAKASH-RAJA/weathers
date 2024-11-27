import os
import shutil
import requests

# Ensure the 'dist' directory exists
os.makedirs('./dist', exist_ok=True)

# OpenWeatherMap API Key
API_KEY = "875cf0ce8bb89560349cf018a48cf066"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# List of cities
CITIES = ["Salem"]

weather_data = []
for city in CITIES:
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "icon": data["weather"][0]["icon"],
            })
        else:
            weather_data.append({"city": city, "error": "Could not fetch data"})
    except Exception as e:
        weather_data.append({"city": city, "error": str(e)})

# HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Information</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f9ff;
            text-align: center;
            padding: 20px;
        }

        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            background: linear-gradient(
                135deg,
                rgba(240, 248, 255, 0.8), 
                rgba(128, 0, 128, 0.8) 
            ); 
            border-radius: 20px; 
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); 
            padding: 20px;
            margin: auto;
            max-width: 80%; 
        }

        .card {
            background: linear-gradient(
                135deg,
                rgba(220, 228, 225, 0.9), 
                rgba(128, 0, 128, 0.11) 
            ); 
            padding: 20px;
            border-radius: 15px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
            transition: transform 0.3s ease, box-shadow 0.3s ease; 
        }

        .card:hover {
            transform: translateY(-10px); 
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .error {
            color: red;
            font-weight: bold;
        }

        img {
            width: 50px;
            height: auto;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>Weather Information</h1>
    <div class="container" id="weatherContainer">
"""

for weather in weather_data:
    if "error" in weather:
        html_content += f"""
        <div class="card">
            <h2>{weather['city']}</h2>
            <p class="error">{weather['error']}</p>
        </div>
        """
    else:
        html_content += f"""
        <div class="card">
            <h2>{weather['city']}</h2>
            <img src="https://openweathermap.org/img/wn/{weather['icon']}@2x.png" alt="Weather Icon">
            <p>Temperature: {weather['temperature']}°C</p>
            <p>{weather['description'].capitalize()}</p>
            <p>Humidity: {weather['humidity']}%</p>
            <p>Wind Speed: {weather['wind_speed']} m/s</p>
        </div>
        """

html_content += """
    </div>
</body>
</html>
"""

# Save the HTML content to the 'dist' directory
html_file_path = "./dist/index.html"
with open(html_file_path, "w") as file:
    file.write(html_content)

# Copy the Python script itself to the 'dist' directory
python_file_path = "./dist/weather_script.py"
shutil.copy(__file__, python_file_path)

print(f"Weather information and script have been saved to './dist' directory.")
