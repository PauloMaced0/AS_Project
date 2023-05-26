from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random
import time

prometheus_pushgateway_url = 'http://pushgateway:9091/'  # Replace with the actual Pushgateway URL

while True:
    registry = CollectorRegistry()
    
    latitude_gauge = Gauge('latitude', 'Latitude metric', registry=registry)
    longitude_gauge = Gauge('longitude', 'Longitude metric', registry=registry)
    altitude_gauge = Gauge('altitude', 'Altitude metric', registry=registry)
    battery_gauge = Gauge('battery', 'Battery metric', registry=registry)

    # Generate random values for the metrics
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    altitude = random.uniform(0, 10000)
    battery = random.uniform(0, 100)

    latitude_gauge.set(latitude)
    longitude_gauge.set(longitude)
    altitude_gauge.set(altitude)
    battery_gauge.set(battery)

    # Push the metrics to the Pushgateway
    push_to_gateway(prometheus_pushgateway_url, job='my_job', registry=registry)

    print(f"Pushed metrics to Pushgateway: latitude={latitude}, longitude={longitude}, altitude={altitude}, battery={battery}")

    time.sleep(1)
