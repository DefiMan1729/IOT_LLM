# LLM running locally on Raspberry Pi 5 with access to IoT sensor Data

## Overview

This project demonstrates how to read temperature data from a DHT11 sensor connected to an Arduino Uno, transmit the data to a Raspberry Pi 5 via a USB connection, and process the data using a locally hosted Large Language Model (LLM).

![IMG20250315170913-COLLAGE](https://github.com/user-attachments/assets/09dff353-f704-43fe-b605-bb106815200f)

---

## Hardware Setup

1. **DHT11 Sensor:**
   - **Data Pin:** Connected to **Pin 2** of the Arduino Uno. (you can choose any data pin)
   - The DHT11 sensor measures temperature data.

2. **Arduino Uno:**
   - Acts as a bridge to transmit the DHT11 sensor data to the Raspberry Pi.
   - Connected to the Raspberry Pi 5 via a **USB cable**. 

3. **Raspberry Pi 5:**
   - Reads the serial data sent by the Arduino Uno.
   - Hosts the Large Language Model (DeepSeek) to process and analyze the temperature data.

---

## Software Setup

### Arduino Code

The following code reads temperature data from the DHT11 sensor and sends it to the Raspberry Pi via serial communication:

```cpp
// Include the DHT11 library for interfacing with the sensor.
#include <DHT11.h>

// Create an instance of the DHT11 class.
// Connect the sensor to Digital I/O Pin 2.
DHT11 dht11(2);

void setup() {
    // Initialize serial communication to allow debugging and data readout.
    Serial.begin(9600);
    
    // Set a custom delay between sensor readings (default is 500ms).
    dht11.setDelay(500);
}

void loop() {
    // Attempt to read the temperature value from the DHT11 sensor.
    int temperature = dht11.readTemperature();

    // Check the result of the reading.
    if (temperature != DHT11::ERROR_CHECKSUM && temperature != DHT11::ERROR_TIMEOUT) {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.println(" °C");
    } else {
        // Print error message based on the error code.
        Serial.println(DHT11::getErrorString(temperature));
    }
}

```

### Python code for Raspberry Pi 5
The following Python script reads temperature data from the Arduino Uno, processes it using the DeepSeek LLM, and logs the response:

```python3
import ollama
import time
import psutil  # Library for CPU and memory statistics
from DHT11 import serial_conn_read  # Import the serial data reading function from DHT11.py

# Define constants
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with your port
BAUD_RATE = 9600  # Communication speed in bits per second
DESIRED_MODEL = 'deepseek-r1:1.5b'  # LLM model name

try:
    # Record the start time to measure response time
    start_time = time.time()

    # Fetch data from the DHT11 sensor via Arduino
    dht11_data = serial_conn_read(SERIAL_PORT, BAUD_RATE)
    if dht11_data is not None:
        print(f"From DHT11: {dht11_data}")
    else:
        print("No data received from DHT11.")

    # Formulate a query for the DeepSeek LLM
    QUESTION_TO_ASK = (
        f"Return a JSON with key as 'temperature' and value as {dht11_data}. "
        f"If the value is more than 30 degrees Celsius, the key 'alert' should be positive, else negative."
    )

    # Send query to the LLM
    response = ollama.chat(
        model=DESIRED_MODEL,
        messages=[
            {
                'role': 'user',
                'content': QUESTION_TO_ASK,
            },
        ]
    )

    # Measure response time
    end_time = time.time()
    response_time = end_time - start_time

    # Extract and display the LLM response
    ollama_response = response['message']['content']
    print("\nLLM Response:")
    print(ollama_response)

    # Collect and display system performance metrics
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage as a percentage
    memory_info = psutil.virtual_memory()
    print("\nSystem Metrics:")
    print(f"Response Time: {response_time:.2f} seconds")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%")

    # Save the LLM response to a file
    with open("OutputOllama.txt", "w", encoding="utf-8") as text_file:
        text_file.write(ollama_response)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Execution completed.")

```
## How to Run

### Set Up the Hardware:
1. Connect the **DHT11 sensor** to **Pin 2** of the Arduino Uno.
2. Connect the **Arduino Uno** to the **Raspberry Pi 5** using a USB cable.

### Upload the Arduino Code:
1. Use the **Arduino IDE** to upload the Arduino sketch provided in the **Arduino Code** section to your Arduino Uno.

### Run the Python Script:
1. On the **Raspberry Pi**, execute the Python script provided in the **Raspberry Pi Code** section to read the temperature data and process it with **DeepSeek**.

