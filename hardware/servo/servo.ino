#include <Servo.h>
Servo servo;

void setup(){  
  Serial.begin(115200);
  servo.attach(2);
  servo.write(90);
}
void loop(){
  long value = 0;

  if (Serial.available()) {
    value = Serial.parseInt(); // 정수만 뽑아서 변수에 넣어주는 함수

      if (value == 1) {
              Serial.println("Left");
              servo.write(35);delay(300);
              servo.write(90);delay(300);
            
      } 
      else if (value == 2){
              Serial.println("Right");
              servo.write(145);delay(300);
              servo.write(90);delay(300);
      }
  }
}
