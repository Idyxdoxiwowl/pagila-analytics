from prometheus_client import start_http_server, Gauge, Counter
import requests
import time
import random

# --- Настройки ---
API_KEY = "9d681cfb761e61870a806921bac779e2"  
CITY = "Astana"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# --- Метрики Prometheus ---
temperature = Gauge('weather_temperature_celsius', 'Current temperature in Celsius')
feels_like = Gauge('weather_feels_like_celsius', 'Feels like temperature in Celsius')
humidity = Gauge('weather_humidity_percent', 'Humidity in percentage')
pressure = Gauge('weather_pressure_hpa', 'Atmospheric pressure in hPa')
wind_speed = Gauge('weather_wind_speed_mps', 'Wind speed in meters per second')
cloudiness = Gauge('weather_cloudiness_percent', 'Cloudiness in percent')
visibility = Gauge('weather_visibility_meters', 'Visibility in meters')
sunrise = Gauge('weather_sunrise_timestamp', 'Sunrise time (UNIX)')
sunset = Gauge('weather_sunset_timestamp', 'Sunset time (UNIX)')
update_time = Gauge('weather_last_update_seconds', 'Last update timestamp')
comfort_index = Gauge('weather_comfort_index', 'Synthetic comfort index combining temperature and humidity')
temperature_variation = Gauge('weather_temp_variation_last_hour', 'Simulated temperature variation last hour')
api_latency = Gauge('weather_api_latency_seconds', 'OpenWeather API response latency in seconds')
api_errors = Counter('weather_api_errors_total', 'Number of API request errors')

# --- Основная функция ---
def collect_weather():
    start = time.time()
    try:
        resp = requests.get(URL, timeout=10)
        latency = time.time() - start
        api_latency.set(latency)

        data = resp.json()

        if resp.status_code != 200 or "main" not in data:
            api_errors.inc()
            print("⚠️ Invalid response:", data)
            return

        main = data["main"]
        wind = data.get("wind", {})
        clouds = data.get("clouds", {})
        sys = data.get("sys", {})

        # Основные метрики
        temperature.set(main.get("temp", 0))
        feels_like.set(main.get("feels_like", 0))
        humidity.set(main.get("humidity", 0))
        pressure.set(main.get("pressure", 0))
        wind_speed.set(wind.get("speed", 0))
        cloudiness.set(clouds.get("all", 0))
        visibility.set(data.get("visibility", 0))
        sunrise.set(sys.get("sunrise", 0))
        sunset.set(sys.get("sunset", 0))
        update_time.set(time.time())

        # Кастомные расчёты
        comfort_index.set(round((main.get("temp", 0) + (100 - main.get("humidity", 0)) / 5), 2))
        temperature_variation.set(random.uniform(-1.5, 1.5))

        print(f"✅ Updated metrics for {CITY}: {main.get('temp', '?')}°C, humidity {main.get('humidity', '?')}%, latency {round(latency, 3)}s")

    except Exception as e:
        api_errors.inc()
        print("❌ Error while collecting data:", e)

# --- Запуск ---
if __name__ == "__main__":
    print("🚀 Starting Custom OpenWeather Exporter on port 8000...")
    start_http_server(8000)
    while True:
        collect_weather()
        time.sleep(20)
