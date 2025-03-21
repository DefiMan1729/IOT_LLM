import ollama
import time
import psutil  # Library for CPU and memory statistics

from DHT11 import serial_conn_read  # Import the serial data reading function from DHT11.py

# Define constants for serial communication and the AI model
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with the actual port connected to the DHT11 sensor
BAUD_RATE = 9600  # Communication speed in bits per second
DESIRED_MODEL = 'deepseek-r1:1.5b'  # AI model to process the input

try:
    # Record the start time to calculate response time later
    start_time = time.time()

    # Fetch data from the DHT11 sensor
    dht11_data = serial_conn_read(SERIAL_PORT, BAUD_RATE)
    if dht11_data is not None:
        print(f"From DHT11: {dht11_data}")
    else:
        print("No data received from DHT11.")

    # Formulate a question or request to send to the Ollama model
    QUESTION_TO_ASK = (
        f"Return a JSON with key as 'temperature' and value as {dht11_data}. "
        f"If the value is more than 30 degrees Celsius, the key 'alert' should be positive, else negative."
    )

    # Send the request to the Ollama model
    response = ollama.chat(
        model=DESIRED_MODEL,
        messages=[
            {
                'role': 'user',
                'content': QUESTION_TO_ASK,
            },
        ]
    )

    # Calculate and record the response time
    end_time = time.time()
    response_time = end_time - start_time

    # Extract and print the model's response
    ollama_response = response['message']['content']
    print("\nOllama Response:")
    print(ollama_response)

    # Collect and display system performance metrics
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage as a percentage
    memory_info = psutil.virtual_memory()  # Memory usage statistics

    print("\nMetrics:")
    print(f"Response Time: {response_time:.2f} seconds")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%")

    # Save the response to a file for logging or future use
    with open("OutputOllama.txt", "w", encoding="utf-8") as text_file:
        text_file.write(ollama_response)

except Exception as e:
    # Handle any errors that may occur during execution
    print(f"An error occurred: {e}")

finally:
    # Code here will always execute, ensuring proper cleanup or final messages
    print("Execution completed.")
