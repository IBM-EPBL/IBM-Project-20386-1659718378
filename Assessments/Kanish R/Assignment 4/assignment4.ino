//Wokwi link : https://wokwi.com/projects/346463039285887572

#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h> 
#define TRIG 12   // what pin we're connected to
#define ECHO 14

#define ORG "nbl97v"
#define DEVICE_TYPE "Distance"
#define DEVICE_ID "Distance"
#define TOKEN "Kanish@2002"


float distance;
long duration;

char server[] = ORG ".messaging.internetofthings.ibmcloud.com";
char publishTopic[] = "iot-2/evt/Distance/fmt/json";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;


WiFiClient wifiClient; 
PubSubClient client(server, 1883, NULL ,wifiClient); 

void PublishData(float distance) {
  mqttconnect();
  String payload;
  if(distance < 100.00)
  {
    payload = "{\"Distance\":";
    payload += distance; payload += ",\"Alert\":\"Alert Distance Less than 100 cm\"";
    payload += "}";
  }
  else
  {
    payload = "{\"Distance\":";
    payload += distance;
    payload += "}";

  }
   
  
  Serial.print("Sending payload: ");
  Serial.println(payload);

  
  if (client.publish(publishTopic, (char*) payload.c_str())) {
    Serial.println("Publish ok");
  } else {
    Serial.println("Publish failed");
  }
  
}
void mqttconnect() {
  if (!client.connected()) {
    Serial.print("Reconnecting client to ");
    Serial.println(server);
    while (!client.connect(clientId, authMethod, token)) {
      Serial.print(".");
      delay(500);
    }
     Serial.println();
  }
}
void wificonnect() //function defination for wificonnect
{
  Serial.println();
  Serial.print("Connecting to ");

  WiFi.begin("Wokwi-GUEST", "", 6);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}



void setup()// configureing the ESP32 
{
  Serial.begin(115200);
  pinMode(TRIG,OUTPUT);
  pinMode(ECHO,INPUT);
  wificonnect();
  mqttconnect();
}

void loop()// Recursive Function
{
  client.loop();
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  duration = pulseIn(ECHO, HIGH);
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  PublishData(distance);
  delay(1000);
  if (!client.loop()) {
  mqttconnect();
  }
 
}


