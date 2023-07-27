// Relay control using the ESP8266 WiFi chip

// Import required libraries
#include <ESP8266WiFi.h>
#include <aREST.h>
#include <aREST_UI.h>

// Create aREST instance
aREST_UI rest = aREST_UI();

// WiFi parameters
const char* ssid = "NRG-4a9m";
const char* password = "123456789aA";

// The port to listen for incoming TCP connections 
#define LISTEN_PORT           80

// Create an instance of the webserver
WiFiServer webserver(LISTEN_PORT);

int ledControl(String command);

void setup(void)
{  
  digitalWrite(5, HIGH);

  // Start Serial (to use the Serial Monitor)
  Serial.begin(115200);
  
  // Create UI
  // Set Page title
  rest.title("Relay Control 1");
  // Create On/Off buttons linked to D1 pin (GPIO5) 
  rest.button(5);

  // Function to be exposed on REST API
  rest.function("led", ledControl);

  // Give name and ID to device
  rest.set_id("1");
  rest.set_name("esp8266");
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the webserver
  webserver.begin();
  Serial.println("Server started");
  
  // Print the IP address
  Serial.println(WiFi.localIP());
  
}

void loop() {
  // Handle REST calls
  WiFiClient client = webserver.available();
  
  if (!client) {
    return;
  }
  while (!client.available()) {
    delay(1);
  }
  rest.handle(client);
}

// Function exposed on REST API (same behaviour as the button)
int ledControl(String command) {
  // Print command
  Serial.println(command);

  // Get state from command
  int state = command.toInt();
  
  // Relay allows current to pass through with low voltage at the input (and vice versa).
  if (state == 0) {
    digitalWrite(5, HIGH);
  }
  else {
    digitalWrite(5, LOW);
  }
  return 1;
}