int speedPin_M1 = 5;     //M1 Speed Control
int speedPin_M2 = 6;     //M2 Speed Control
int directionPin_M1 = 4;     //M1 Direction Control
int directionPin_M2 = 7;     //M1 Direction Control


void setup() {
  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){
    int data;
    data = Serial.read();
    Serial.print("Hello, you sent me: ");
    Serial.println(data);
    advance(data);
  }
}

void advance(int data) {
   int spe = 150;
   if (data == 1){
    carAdvance(spe,spe);
   }
   if (data == 2){
    carBack(spe, spe);
    
   if(data == 9){
    carStop();
    delay(500);
    carAdvance(spe,spe);
    delay(1000);
   }
    
    
   }
   if (data == 3){
    carTurnLeft(180,180);
    
   
   }
   if (data == 4){
    carTurnRight(180,180);
    
   }
   if (data == 0 ){
    carStop();
    delay(3000);
    
   }
}


void carStop(){                 //  Motor Stop
  digitalWrite(speedPin_M2,0);
  digitalWrite(directionPin_M1,LOW);
  digitalWrite(speedPin_M1,0);
  digitalWrite(directionPin_M2,LOW); 
}

void carAdvance(int leftSpeed,int rightSpeed){         //Move backward
  analogWrite (speedPin_M2,leftSpeed);              //PWM Speed Control
  digitalWrite(directionPin_M1,HIGH);
  analogWrite (speedPin_M1,rightSpeed);
  digitalWrite(directionPin_M2,HIGH);
}

void carBack(int leftSpeed,int rightSpeed){       //Move forward
  analogWrite (speedPin_M2,leftSpeed);
  digitalWrite(directionPin_M1,LOW);
  analogWrite (speedPin_M1,rightSpeed);
  digitalWrite(directionPin_M2,LOW);
}

void carTurnRight(int leftSpeed,int rightSpeed){      //Turn Left
  analogWrite (speedPin_M2,leftSpeed);
  digitalWrite(directionPin_M1,LOW);
  analogWrite (speedPin_M1,rightSpeed);
  digitalWrite(directionPin_M2,HIGH);
}
void carTurnLeft(int leftSpeed,int rightSpeed){      //Turn Right
  analogWrite (speedPin_M2,leftSpeed);
  digitalWrite(directionPin_M1,HIGH);
  analogWrite (speedPin_M1,rightSpeed);
  digitalWrite(directionPin_M2,LOW);
}
