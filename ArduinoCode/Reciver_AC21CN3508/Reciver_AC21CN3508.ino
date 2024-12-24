/*********************************
   Program For receive data form IC AC21CN3508 (Blood Presure Sensor)
   Option: -
   MCU    : ESP32
   Write By : Panya Hantula
   Date: 7 Dec 2024
   Code version: V.1
   Note: -
 **********************************/

#define Code_Version "V.1.1"
#include <stdio.h>
#include <string.h>

#define SW_PWR 5
#define LED 2

//******* CN3508 Serial Config *********
#define CN3508 Serial2
#define RXD2 16
#define TXD2 17

String CMD_Income;
//******* Setup *******
void setup() {
  Serial.begin(115200);
  Serial.println("AC21CN3508 (Blood Presure Monitering)");
  Serial.print("Code Version:");
  Serial.println(Code_Version);
  // Serial.print("\n\n***********************\n");
  Serial.println("#: Config Serial 2");

  CN3508.begin(115200, SERIAL_8N1, RXD2, TXD2);
  Serial.println("Serial Txd is on pin: " + String(TXD2));
  Serial.println("Serial Rxd is on pin: " + String(RXD2));

  pinMode(SW_PWR, OUTPUT);
  pinMode(LED, OUTPUT);
  digitalWrite(SW_PWR, HIGH);

  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500);

  Serial.print("#:Initializing OK !!!\n\n");
}

//*******  Main Loop *******
void loop() {
  if (Serial.available() > 0) {
    CMD_Income = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(CMD_Income);

    if (CMD_Income.equals("start")) {
      Serial.println("Start Measur Blood Presure");
      digitalWrite(LED, HIGH);
      digitalWrite(SW_PWR, LOW);
      delay(1000);
      digitalWrite(LED, LOW);
      digitalWrite(SW_PWR, HIGH);
      delay(100);

      Serial.println("Read BP data form RAK283 Device");
      //Serial.print("incomingByte: ");
      while (CMD_Income.equals("start"))
        Read_BP_data();
    }
  }
}

//******* Get_BP_data Function *******
void Read_BP_data() {  //******* BP Config *********
  int pos = 0, stringplace = 0;
  String receive_data_ALL[5], String_BP_value, BP_value[14];
  // int heart_rate = 60, sys_rate = 120, dia_rate = 80;
  int heart_rate, sys_rate, dia_rate;
  int incomingByte = 0;

  while (CN3508.available() > 0) {  // wait serial to send data form RAK283
    incomingByte = CN3508.read();
    Serial.print(char(incomingByte));
  }

  if (CN3508.find("find a space:")) {              // Find Text "find a space:" and get string that is end to "!"
    String BuffMsg = CN3508.readStringUntil('!');  // Incoming data
    Serial.print("#: RAK283 Data: ");
    Serial.println(BuffMsg);

    for (int i = 0; i < BuffMsg.length(); i++) {  // Separate string receive data
      if (BuffMsg.substring(i, i + 1) == "\n") {
        receive_data_ALL[pos] = BuffMsg.substring(stringplace, i);
        stringplace = i + 1;
        pos++;
      }
    }
    String_BP_value = receive_data_ALL[2];  // get String BP value
    //Serial.print("#: BP data form RAK283 : ");
    //Serial.println(String_BP_value);
    pos = 0;
    for (int i = 0; i < 14; i++) {  // Separate String BP value
      BP_value[i] = String_BP_value.substring(pos, pos + 2);
      pos += 3;
      // Serial.println(BP_value[i]);
    }

    // Convert Hex to Dec
    sys_rate = HEX2DEX(BP_value[0]);
    dia_rate = HEX2DEX(BP_value[1]);
    heart_rate = HEX2DEX(BP_value[3]);

    // End of the Process
    delay(1000);
    digitalWrite(LED, HIGH);
    digitalWrite(SW_PWR, LOW);
    delay(1000);
    digitalWrite(LED, LOW);
    digitalWrite(SW_PWR, HIGH);
    delay(100);

    Serial.print("SYS:");
    Serial.print(sys_rate);
    Serial.print(",DIA:");
    Serial.print(dia_rate);
    Serial.print(",PUL:");
    Serial.print(heart_rate);
    Serial.print("\n");
    Serial.println("Done");

    CMD_Income = "";
    // sys_rate = 0;
    // dia_rate = 0;
    // heart_rate = 0;
    //Serial.println("End of Process !!");
  }
}

//******* HEX2DEX *******
int HEX2DEX(String String_HEX) {
  char char_array[3];
  int x;
  char *endptr;

  String_HEX.toCharArray(char_array, 3);
  x = strtol(char_array, &endptr, 16);
  //Serial.println(x, HEX);
  //Serial.println(x, DEC);
  return x;
}