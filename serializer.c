#include <Arduino_FreeRTOS.h>
#include <Wire.h>

struct IMU_data {
   int16_t AcX;
   int16_t AcY;
   int16_t AcZ;
   int16_t GyX;
   int16_t GyY;
   int16_t GyZ;
};

// instanciate one struct
struct IMU_data data;



// length of the structure
int IMU_data_len = sizeof(IMU_data);

// send the structure giving the IMU state through serial
void send_IMU_struct() {
  Serial.println("Sending: S");
  Serial1.write('S');
  Serial.println("Sending: E");
//  Serial1.write((uint8_t *)&data, IMU_data_len);
  Serial1.write('E');
  return;
}


// how often should sample

//unsigned long interval_sampling_micro = 10000L; // 100 HZ

//unsigned long interval_sampling_micro = 20000L; // 50 HZ

//unsigned long interval_sampling_micro = 50000L; // 20 HZ

//unsigned long interval_sampling_micro = 100000L; // 10 HZ

unsigned long interval_sampling_micro = 1000000L; // 1 HZ

unsigned long time_previous;

unsigned long time_current;

int handshake_flag = 0;

int packet_type = 0;

byte ACK = 0;
byte SYN = 1;
byte SYN_ACK = 2;
byte DATA_R = 3;
byte DATA_S = 4;


void setup() {

  delay(2000);

  Serial.begin(115200);
  Serial.println("Begin");
  Serial1.begin(115200);
  Serial.print(F("size of struct: "));
  Serial.print(IMU_data_len);
  Serial.println();
  Serial.println(F("done with setup"));



  time_previous = micros();

  data.AcX = 1;
  data.AcY = 2;
  data.AcZ = 3;
  data.GyX = 4;
  data.GyY = 5;
  data.GyZ = 6;

}


int response = 0;

void handle_handshake(int skip) {
  while (handshake_flag == 0) {
//    Serial.println("Waiting for SYN");
//    if (skip) { // we already received SYN
//      Serial1.print(SYN-ACK);
//      skip = 0;
//    } else
    if (Serial1.available()) {
      response = Serial1.read();
      Serial.print(response);
      if (response == SYN) { // raspberry pi wants to perform handshake
        Serial.println("SYN Detected");
        Serial1.print(SYN_ACK);
      } else if (response == ACK) {
        handshake_flag = 1;
        Serial.println("Handshake completed");
      }
    }
  }
}

void loop() {
  handle_handshake(0);
//  if (Serial1.available()) {
//    packet_type = Serial1.read();
//    Serial.println(packet_type);
//    if (packet_type == SYN) { // raspberry pi wants to perform handshake
//      Serial.println("SYN Detected");
//      handle_handshake(1);
//    }
//  }

//  Serial.println("Sending");
  time_previous += interval_sampling_micro;

  // transmit the struct

//  send_IMU_struct();

}
