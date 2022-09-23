#include <SoftwareSerial.h>
#include <MHZ19.h>

SoftwareSerial ss(D3,D4); //Rx Tx
MHZ19 mhz(&ss);

void setup()
{
  Serial.begin(115200);
  ss.begin(9600);
}

void loop(){
  long value = 0;
  if (Serial.available()) {
    value = Serial.parseInt();
  }

  if (value == 1) {
    getCO2();
  }
}

void getCO2() {
  MHZ19_RESULT response = mhz.retrieveData();
  if (response == MHZ19_RESULT_OK)
  {
    Serial.println(mhz.getCO2());
  }
  else
  {
    Serial.print(F("Error, code: "));
    Serial.println(response);
  }
}
