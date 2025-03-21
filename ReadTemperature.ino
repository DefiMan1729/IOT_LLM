// Include the DHT11 library for interfacing with the sensor.
#include <DHT11.h>

// HW setup
// - For Arduino: Connect the sensor to Digital I/O Pin 2.
// Connect the serial cable to Raspberry PI USB

DHT11 dht11(2);

void setup() {
    // Initialize serial communication to allow debugging and data readout.
    // Using a baud rate of 9600 bps.
    Serial.begin(9600);
    
    // Uncomment the line below to set a custom delay between sensor readings (in milliseconds).
    dht11.setDelay(500); // Set this to the desired delay. Default is 500ms.
}

void loop() {
    // Attempt to read the temperature value from the DHT11 sensor.
    int temperature = dht11.readTemperature();
    if (temperature != DHT11::ERROR_CHECKSUM && temperature != DHT11::ERROR_TIMEOUT) {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.println(" °C");
    } else {
        // Print error message based on the error code.
        Serial.println(DHT11::getErrorString(temperature));
    }
}
