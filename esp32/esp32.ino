const int leadsOff1 = 15;
const int leadsOff2 = 2;



void setup() {
    // initialize serial communication at 115200 bits per second:
    Serial.begin(115200);
    
    //set the resolution to 12 bits (0-4096)
    //analogReadResolution(12);
    pinMode(leadsOff1, INPUT); // Setup for leads off detection LO +
    pinMode(leadsOff2, INPUT); // Setup for leads off detection LO -     
}
     
void loop() {
     
    if((digitalRead(leadsOff1) == 1)||(digitalRead(leadsOff2) == 1) || (analogRead(A0) < 50)){
      Serial.println('!');
    }
    else{
      // send the value of analog input 0:
      Serial.println(analogRead(34));
    }
    //Wait for a bit to keep serial data from saturating
    delay(1);
}
