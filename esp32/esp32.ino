#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

// Replace the next variables with your SSID/Password combination
const char* ssid = "";
const char* password = "";

// Add your MQTT Broker IP address, example:
const char* mqtt_server = "192.168.1.52";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
char str_sensor[10];
const int leadsOff1 = 15;
const int leadsOff2 = 2;
String bulkSend = "";



void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* message, unsigned int length) {
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 1) {
    lastMsg = now;

    if((digitalRead(leadsOff1) == 1)||(digitalRead(leadsOff2) == 1)){
        Serial.println('!');
        bulkSend += "!\n";
        client.publish("/datatomusic", "!");

    }
    else {
      float sensor = analogRead(34);
      /* 4 is minimum width, 2 is precision; float value is copied onto str_sensor*/
      dtostrf(sensor, 4, 1, str_sensor);
      bulkSend += str_sensor;
      bulkSend += "/n";
      //Serial.println(str_sensor);
      //client.publish("/datatomusic", str_sensor);
    }
  }
  if (bulkSend.length() > 500) {
      Serial.println("publishinggggggggggggggggggggggggggggggggggggg");
      Serial.println(bulkSend);
      char charArray[bulkSend.length() + 1];  // +1 to account for the null-terminator
      bulkSend.toCharArray(charArray, sizeof(charArray));
      client.publish("/datatomusic", charArray);
      bulkSend = "";
  }

}