#include <Servo.h>
Servo base,farm,zarm,claw;
int pos=0;


void setup() {
  base.attach(11);
  zarm.attach(10);
  farm.attach(9);
  claw.attach(5);

  base.write(90);
  zarm.write(10);
  farm.write(90);
  claw.write(40);


  Serial.begin(9600);
  Serial.println("Start");
  
  
  // put your setup code here, to run once:

}
int a0, a1, a2, a3 = 0;
int base_pos,farm_pos,zarm_pos,claw_pos = 0;
void loop() {
  a0 = analogRead(0);
  a1 = analogRead(1);
  a2 = analogRead(2);
  a3 = analogRead(3);

  base_pos = map(a0, 0, 1023, 0, 180);
  farm_pos = map(a1, 0, 1023, 10, 140);
  zarm_pos = map(a2, 0, 1023, 20, 180);
  claw_pos = map(a3, 0, 1023, 40, 140);

  base.write(base_pos);
  zarm.write(zarm_pos);
  farm.write(farm_pos);
  claw.write(claw_pos);
  
  Serial.print(a0);
  Serial.print(' ');
  Serial.print(a1);
  Serial.print(' ');
  Serial.print(a2);
  Serial.print(' ');
  Serial.println(a3);



}
