import network
import socket
import machine
import time
import math


# Define the LED pin
led_pin = machine.Pin("LED", machine.Pin.OUT)

ssid = 'Radek_nej.cz'
password = '605884396'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)


# Wait for connection or fail
max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(2)

# Handle connection error
if not wlan.isconnected():
    raise RuntimeError('Network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP:', status[0])

html_content = """
<!DOCTYPE html>
<html>

<head>
    <title>Raspberry Pi Pico Temperature Monitoring</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-items: center;
        }
        p{
        font-size:large;
        /* font-weight: bolder; */
        border: 1px solid gray;
        padding: 5px;
        }
        
        #choices{
            flex-direction: row;
        }
        button {
            max-width: 100px;
            height: 50px;
            margin: 1em;
            font-weight: bold;
        }
    </style>
    <script>
        var intervalID;

        // Function to start displaying temperature in Celsius
        function startCelsius() {
            clearTemperature()  // Stop refresh if it's running
            intervalID = setInterval(updateTemperatureCelsius, 800);
        }

        // Function to start displaying temperature in Fahrenheit
        function startFahrenheit() {
            clearTemperature()  // Stop refresh if it's running
            intervalID = setInterval(updateTemperatureFahrenheit, 800);
        }
        
        // Function to start displaying temperature in Kelvin
        function startKelvin() {
            clearTemperature()  // Stop refresh if it's running
            intervalID = setInterval(updateTemperatureKelvin, 800);
        }

        // Function to clear the temperature refresh
        function clearTemperature() {
            clearInterval(intervalID);
        }
        
        function stopRefresh(){
            clearInterval(intervalID);
            fetch('/stopLED', { method: 'POST' })
        }

        // Function to update temperature in Celsius dynamically
        function updateTemperatureCelsius() {
            updateTemperature("/Celsius");
        }

        // Function to update temperature in Fahrenheit dynamically
        function updateTemperatureFahrenheit() {
            updateTemperature("/Fahrenheit");
        }
        
        // Function to update temperature in Kelvin dynamically
        function updateTemperatureKelvin() {
            updateTemperature("/Kelvin");
        }

        // Function to update temperature dynamically
        function updateTemperature(url) {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("temperature").innerHTML = this.responseText;
                }
            };
            xhttp.open("GET", url, true);
            xhttp.send();
        }
        window.onload = stopRefresh;
    </script>
</head>

<body>
    <h1>Raspberry Pi Pico Temperature Monitoring</h1>
    <p><span id="temperature">Loading...</span></p>
    <div id="choices">
        <button onclick="startCelsius()">Show Celsius</button>
        <button onclick="startFahrenheit()">Show Fahrenheit</button>
        <button onclick="startKelvin()">Show Kelvin</button>
    </div>
    <button onclick="stopRefresh()">Stop Refresh</button>
</body>
</html>
"""

def http_response(status_code, content):
    return 'HTTP/1.0 {status_code}\r\nContent-Type: text/html\r\nContent-Length: {content_length}\r\n\r\n{content}'.format(
        status_code=status_code,
        content_length=len(content),
        content= content
    )

def web_server():
    # Create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80))  # Bind to port 80
    s.listen(5)  # Listen for incoming connections

    # Define LED pin
    led_pin = machine.Pin("LED", machine.Pin.OUT)  # Assuming GPIO pin 25 is connected to the LED

    while True:
        state = "Click the buttons above to toggle the LED."
        conn, addr = s.accept()  # Accept a new connection
        print('Connection from:', addr)
        
        request = conn.recv(1024).decode('utf-8')  # Receive the HTTP request
        print('Request:', request)

        # Check if request is for temperature in Celsius
        if 'GET /Celsius' in request:
            temperature = get_celsius()
            led_pin.on()  # Turn on LED when temperature is being displayed
            response = http_response(200, str(temperature) + " °C")
            
        # Check if request is for temperature in Fahrenheit    
        elif 'GET /Fahrenheit' in request:
            temperature = get_fahrenheit()
            led_pin.on()  # Turn on LED when temperature is being displayed
            response = http_response(200, str(temperature) + " °F")
        
        # Check if request is for temperature in Kelvin    
        elif 'GET /Kelvin' in request:
            temperature = get_kelvin()
            led_pin.on()  # Turn on LED when temperature is being displayed
            response = http_response(200, str(temperature) + " K")
            
        # Check for Stop request   
        elif 'POST /stopLED' in request:
            led_pin.off()
            response = http_response(200, "LED stop acknowledged")
        else:
            # Return HTML page
            response = http_response(200, html_content)
        
        conn.send(response.encode('utf-8'))  # Send HTTP response
        conn.close()   # Close the connection


def get_celsius():
    # Read ADC value from temperature sensor
    adc_value = machine.ADC(4).read_u16()  # GPIO pin 4 is connected to the temperature sensor

    # Convert ADC value to temperature in degrees Celsius
    conversed = adc_value  * 3.3/65535
    temperature = 27 - (conversed - 0.706) / 0.001721

    return round(temperature, 2)  # Round to 2 decimal places

def get_fahrenheit():
    # Read ADC value from temperature sensor
    adc_value = machine.ADC(4).read_u16()  # GPIO pin 4 is connected to the temperature sensor

    # Convert ADC value to temperature in degrees Fahrenheit
    conversed = adc_value  * 3.3/65535
    temperature = 80.6 - 1.8*(conversed - 0.706)/0.001721

    return round(temperature, 2)  # Round to 2 decimal places

def get_kelvin():
    adc_value = machine.ADC(4).read_u16()  # GPIO pin 4 is connected to the temperature sensor

    # Convert ADC value to temperature in degrees Kelvin
    conversed = adc_value  * 3.3/65535
    temperature = 300.15 - (conversed - 0.706)/0.001721

    return round(temperature, 2)

# Run the web server
web_server()
