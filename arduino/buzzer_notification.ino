// Listens for data over serial connection and
// plays beep on the buzzer

#ifndef SERIAL_RATE
#define SERIAL_RATE     115200
#endif

#ifndef SERIAL_TIMEOUT
#define SERIAL_TIMEOUT  5
#endif

int buzzer_pin = 13;
int frequency = 200;
int duration = 100;

void setup(){
  Serial.begin(SERIAL_RATE);
  Serial.setTimeout(SERIAL_TIMEOUT);
}

void loop(){
 while (Serial.available() > 0) {
   switch(Serial.parseInt()){
     case 1:
       while (Serial.parseInt() != 99) {
         tone(buzzer_pin, frequency, duration);
         delay(2000);
       }
       noTone(buzzer_pin);
     case 99:
	// do nothing, to stop any previous operation
        break;
   }
 } 
}
