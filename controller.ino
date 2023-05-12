#include <Stepper.h>

const int stepsPerRevolution = 30;

Stepper stepper1(stepsPerRevolution, 5,4,3,2);
Stepper stepper2(stepsPerRevolution, 6, 7, 8, 9);


class SR04{
  int trigPin;
  int echoPin;

  public:
  SR04(int trig, int echo){
    trigPin = trig;
    echoPin = echo;

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
  }

  long distance(){
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);

    return duration * 0.034 / 2; // in centimeter
  }
};

SR04 sensor6(46, 47);
SR04 sensor5(42, 43);
SR04 sensor4(38, 39);
SR04 sensor3(34, 35);
SR04 sensor2(30, 31);
SR04 sensor1(26, 27);

int incomingByte = 0;

int STEPPERDELAY = 4000;


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  stepper1.setSpeed(60);
  stepper2.setSpeed(60);
}

void loop() {

  // long distance1 = sensor1.distance();
  // long distance2 = sensor2.distance();
  // long distance3 = sensor3.distance();
  // long distance4 = sensor4.distance();
  // long distance5 = sensor5.distance();

  // Serial.print(distance1);
  // Serial.print("\t");
  // Serial.print(distance2);
  // Serial.print("\t");
  // Serial.print(distance3);
  // Serial.print("\t");
  // Serial.print(distance4);
  // Serial.print("\t");
  // Serial.print(distance5);
  // Serial.println("\t");

  // delay(50);

  if (Serial.available() > 0) {
    incomingByte = Serial.read();

    if (incomingByte){

      stepper1.step(stepsPerRevolution);
      stepper2.step(-stepsPerRevolution);
      delay(STEPPERDELAY);

      // sensor excecution
      long distance1 = sensor1.distance();
      long distance2 = sensor2.distance();
      long distance3 = sensor3.distance();
      long distance4 = sensor4.distance();
      long distance5 = sensor5.distance();

      String text = String(distance1) + "," + String(distance2) + "," + String(distance3) + "," + String(distance4) + "," + String(distance5);

      Serial.println(text);

      stepper1.step(-stepsPerRevolution);
      stepper2.step(stepsPerRevolution);
    }
  }

}