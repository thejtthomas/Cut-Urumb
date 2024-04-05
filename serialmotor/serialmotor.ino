//
// serialstep.ino
//
// serial step-and-direction
//
// Neil Gershenfeld 4/11/21
// Quentin Bolsee 12/7/21 : add button
//
// This work may be reproduced, modified, distributed,
// performed, and displayed for any purpose, but must
// acknowledge this project. Copyright is retained and
// must be preserved. The work is provided as is; no
// warranty is provided, and users accept all liability.
//

#define LEDA 30
#define LEDC 14
#define EN 5
#define DIR 2
#define STEP 4


#define BUTTON 31

void setup() {
   SerialUSB.begin(0);
   digitalWrite(LEDA,HIGH);
   pinMode(LEDA,OUTPUT);
   digitalWrite(LEDC,LOW);
   pinMode(LEDC,OUTPUT);
   digitalWrite(EN,LOW);
   pinMode(EN,OUTPUT);
   digitalWrite(STEP,LOW);
   pinMode(STEP,OUTPUT);
   digitalWrite(DIR,LOW);
   pinMode(DIR,OUTPUT);
   pinMode(BUTTON, INPUT_PULLUP);
   /*
   // 1 step
   digitalWrite(M0,LOW);
   digitalWrite(M1,LOW);
   pinMode(M0,OUTPUT);
   pinMode(M1,OUTPUT);
   // 1/2 step
   digitalWrite(M0,HIGH);
   digitalWrite(M1,LOW);
   pinMode(M0,OUTPUT);
   pinMode(M1,OUTPUT);
   */
   // 1/8 step
  //  digitalWrite(M0,HIGH);
  //  digitalWrite(M1,HIGH);
  //  pinMode(M0,OUTPUT);
  //  pinMode(M1,OUTPUT);
   /*
   // 1/16 step
   digitalWrite(M1,HIGH);
   pinMode(M0,INPUT);
   pinMode(M1,OUTPUT);
   // 1/32 step
   digitalWrite(M0,LOW);
   pinMode(M0,OUTPUT);
   pinMode(M1,INPUT);
   */
   }

void loop() {
   if (SerialUSB.available()) {
      char c = SerialUSB.read();
      if (c == 'f') {
         digitalWrite(DIR,HIGH);
         digitalWrite(STEP,HIGH);
         delayMicroseconds(4);
         digitalWrite(STEP,LOW);
         }
      else if (c == 'r') {
         digitalWrite(DIR,LOW);
         digitalWrite(STEP,HIGH);
         delayMicroseconds(4);
         digitalWrite(STEP,LOW);
         }
      else if (c == '?') {
         // reply with button value
         int btn = digitalRead(BUTTON);
         SerialUSB.write(btn ? '1' : '0');
         }
      else if (c == '@') {
         SerialUSB.write("0000");
         }
      }
   }