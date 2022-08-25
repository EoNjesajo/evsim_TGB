#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <SoftwareSerial.h>
#include <MHZ19.h>

#define HOME_SSID "SSID 입력"
#define HOME_PWD "PWD 입력"

ESP8266WebServer server(80);

SoftwareSerial ss(D3,D4); //Rx Tx
MHZ19 mhz(&ss);

void setup()
{
  Serial.begin(115200);
  Serial.println(F("Starting...")); 

  ss.begin(9600);

  WiFi.begin(HOME_SSID, HOME_PWD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", check_sensor);
  server.begin();
  Serial.println("Server listening");
}

void loop() {
  server.handleClient();
}

// 시리얼 모니터로 정보 조회
//void loop(){
//  long value = 0;
//
//  if (Serial.available()) {
//    value = Serial.parseInt();
//  }
//
//  if (value == 1) {
//
//    MHZ19_RESULT response = mhz.retrieveData();
//    if (response == MHZ19_RESULT_OK)
//    {
//      Serial.print(F("CO2: "));
//      Serial.println(mhz.getCO2());
//      Serial.print(F("Min CO2: "));
//      Serial.println(mhz.getMinCO2());
//      Serial.print(F("Temperature: "));
//      Serial.println(mhz.getTemperature());
//      Serial.print(F("Accuracy: "));
//      Serial.println(mhz.getAccuracy());
//    }
//    else
//    {
//      Serial.print(F("Error, code: "));
//      Serial.println(response);
//    }
//  }
//}

// 웹에서 정보 확인
void check_sensor() {
  MHZ19_RESULT response = mhz.retrieveData();
  if (response == MHZ19_RESULT_OK) {
    int sensor = mhz.getCO2();
    String co2 = String(sensor);
    server.send(200, "text/html", "co2: " + co2);
  }
  else {
    Serial.print(F("Error, code: "));
    Serial.println(response);
  }
}
