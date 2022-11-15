#include <Servo.h>
#include <SoftwareSerial.h>   // 引用程式庫
#include  <Wire.h>
// 定義連接藍牙模組的序列埠
SoftwareSerial BT(12,13); //傳送腳,接收腳

Servo base,farm,zarm,claw;
int pos=0;


void setup() {
  base.attach(11);
  zarm.attach(10);
  farm.attach(9);
  claw.attach(5);

  base.write(90);
  zarm.write(90);
  farm.write(90);
  claw.write(40);

  Serial.begin(9600);
  Serial.println("Start");

  BT.begin(38400);  
  // put your setup code here, to run once:

}

int base_pos = 90;
int farm_pos = 90;
int zarm_pos = 90;
int claw_pos = 90;
char R_Data[10];

int kn = 0;
void loop() {
  if (BT.available()>0) {
    char serialcmd = BT.read();
    armDataCmd(serialcmd); 
  }

  base.write(base_pos); 
  farm.write(farm_pos); 
  zarm.write(zarm_pos); 
  claw.write(claw_pos);
  delay(1);
}
void armDataCmd(char serialCmd){
   
  Serial.print("serialCmd = ");
  Serial.print(serialCmd);  
 
  int servoData = BT.parseInt(); 
  switch(serialCmd){
    case 'b':  
      base_pos = servoData;
      Serial.print("  Set base servo value: ");
      Serial.println(servoData);
      break;
    case 'c':  
      claw_pos = servoData;
      Serial.print("  Set claw servo value: ");
      Serial.println(servoData);
      break;
    case 'f':  
      farm_pos = servoData;
      Serial.print("  Set fArm servo value: ");
      Serial.println(servoData);
      break;
    case 'z':  
      zarm_pos = servoData;
      Serial.print("  Set rArm servo value: ");
      Serial.println(servoData);
      break;
    case 'o':  
      reportStatus();
      break;
    default:
      Serial.println(" Unknown Command.");
  }  
 
}
 void reportStatus(){
  Serial.println("");
  Serial.println("");
  Serial.println("++++++ Robot-Arm Status Report +++++");
  Serial.print("Claw Position: clawPos = "); Serial.println(claw.read());
  Serial.print("Base Position: basePos = "); Serial.println(base.read());
  Serial.print("Rear  Arm Position: rarmPos = "); Serial.println(zarm.read());
  Serial.print("Front Arm Position: farmPos = "); Serial.println(farm.read());
  Serial.println("++++++++++++++++++++++++++++++++++++");
  Serial.println("");
 }
