#include <Arduino_FreeRTOS.h>
#include <semphr.h>  // add the FreeRTOS functions for Semaphores (or Flags).
#include <CircularBuffer.h>
#include <CRC32.h>
#include <Wire.h>
#include <MPU6050.h>

#define STACK_DEPTH 128
#define PERIOD 32 
// https://arduino.stackexchange.com/questions/9899/serial-structure-data-transfer-between-an-arduino-and-a-linux-pc
struct __attribute__ ((packed)) IMU_data {
    int16_t Ac1X;          
    int16_t Ac1Y;
    int16_t Ac1Z;
    int16_t Gy1X;
    int16_t Gy1Y;
    int16_t Gy1Z;
    int16_t Ac2X;          
    int16_t Ac2Y;
    int16_t Ac2Z;
    int16_t Gy2X;
    int16_t Gy2Y;
    int16_t Gy2Z;
    int16_t Ac3X;          
    int16_t Ac3Y;
    int16_t Ac3Z;
    int16_t Gy3X;
    int16_t Gy3Y;
    int16_t Gy3Z;
    uint32_t checksum;
}; 

struct __attribute__ ((packed)) power_data {
    int16_t voltage;
    int16_t current;
    int16_t power;
    int16_t checksum;
}; 

// Arduino code version 2 starts here
//MPU6050 MPU_ARM;
//MPU6050 MPU_LEG;
//MPU6050 MPU_TORSO;
MPU6050 accelgyro;

CircularBuffer<IMU_data,5> IMU_data_buffer; 

SemaphoreHandle_t xSemaphore_IMU = NULL;
SemaphoreHandle_t xSemaphore_power = NULL;

const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.
const int sensor1 = 22;
const int sensor2 = 24;
const int sensor3 = 26;

int16_t accelerometer_x, accelerometer_y, accelerometer_z;   // variables for accelerometer raw data
int16_t gyro_x, gyro_y, gyro_z;                             // variables for gyro raw data
int16_t temperature;                                      // variables for temperature data

// instantiate one struct
IMU_data data;
IMU_data* data_ptr = &data;
power_data p_data;

// length of the structures
int IMU_data_len = sizeof(IMU_data);
int power_data_len = sizeof(power_data);

// instantiate buffer
uint8_t byteBuffer[36];

int handshake_flag = 0;

byte ACK = 0;
byte SYN = 1;
byte SYN_ACK = 2;
byte DATA_R = 3;
byte DATA_P = 4;
byte EMPTY = 5;

// send the structure giving the IMU state through serial
void send_IMU_struct() {
//    Serial.println("Sending Sensor Data");
//    Serial.println("Sending: S");
 
//    Serial.println("Sending: E");
    if (!IMU_data_buffer.isEmpty()) {
      data = IMU_data_buffer.shift();
      Serial1.write('S');
      Serial1.write((uint8_t *)&data, IMU_data_len);
      Serial1.write('E');
    } else {
      Serial.println("Buffer is empty");
      Serial1.write(EMPTY);
    }

    return;
}

// send the structure giving the IMU state through serial
void send_power_struct() {
    Serial.println("Sending: S");
    Serial1.write('S');
    Serial.println("Sending: E");
    Serial1.write((uint8_t *)&p_data, power_data_len);
    Serial1.write('E');
    return;

}

/**
 * Retrieve data from sensors
 */
void retrieveSensorData(void *p){
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = PERIOD / 2;
     
    for(;;) {
        if( xSemaphore_IMU != NULL ){
            /* See if we can obtain the semaphore.  If the semaphore is not
               available wait 10 ticks to see if it becomes free. */
            if( xSemaphoreTake( xSemaphore_IMU, ( TickType_t ) 10 ) == pdTRUE )
            {
                /* We were able to obtain the semaphore and can now access the
                   shared resource. */

                /* ... */
                getData(1, &data);
                getData(2, &data);
                getData(3, &data);

                size_t buffer_length = sizeof(byteBuffer);

                char* data_bytes = (char*) data_ptr;
                
                for( size_t i = 0; i < buffer_length; i++ ) {
                  byteBuffer[i] = data_bytes[i];
                }
              
                data.checksum = CRC32::calculate(byteBuffer, 36);

                IMU_data_buffer.push(data);

                int buffer_size = IMU_data_buffer.size();
                Serial.print("buffer size: ");
                Serial.println(buffer_size);
                /* We have finished accessing the shared resource.  Release the
                   semaphore. */
                xSemaphoreGive( xSemaphore_IMU );
            }
            else
            {
                /* We could not obtain the semaphore and can therefore not access
                   the shared resource safely. */
            }
        }
        
        vTaskDelayUntil(&xLastWakeTime, xFrequency / portTICK_PERIOD_MS);
    }

    

}

/**
 * Retrieve data from power management system
 */
void retrievePowerData(void *p){
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = PERIOD * 4;

    for(;;){
//        delay(DELAY_AMT);
        if( xSemaphore_power != NULL ){
            /* See if we can obtain the semaphore.  If the semaphore is not
               available wait 10 ticks to see if it becomes free. */
            if( xSemaphoreTake( xSemaphore_power, ( TickType_t ) 10 ) == pdTRUE )
            {
                /* We were able to obtain the semaphore and can now access the
                   shared resource. */
//                Serial.println("Retrieving Power Data, 1");
                /* ... */

                /* We have finished accessing the shared resource.  Release the
                   semaphore. */
                xSemaphoreGive( xSemaphore_power );
            }
            else
            {
                /* We could not obtain the semaphore and can therefore not access
                   the shared resource safely. */
            }
        }

        vTaskDelayUntil(&xLastWakeTime, xFrequency / portTICK_PERIOD_MS);
    }

    

}

int response = 0;

void handle_handshake() {

    while (handshake_flag == 0) {
        Serial.println("Handshaking");
        delay(300);
        if (Serial1.available()) {
            response = Serial1.read();    // From RPI to arduino   
            if (response == SYN) { // raspberry pi wants to perform handshake
                //        Serial.println("Sending SYN_ACK");
                Serial1.print(SYN_ACK);     // From arduino to RPI
            } else if (response == ACK) {
                handshake_flag = 1;
                Serial.println("Handshake completed");
            }
        }
    }
}

/**
 * Handle inputs from raspberry PI
 */
void handleInput(void *p){
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = PERIOD / 16;
    int input;
    for(;;){
        if (Serial1.available()) { // if there is an available byte..
            input = Serial1.read();  // read it
            if (input == SYN) {      // RPI is trying to initiate handshake
                Serial.println("RPI input: handshake");
                handshake_flag = 0;
                handle_handshake();
            } else if (input == DATA_R) { // RPI is requesting data
                if (handshake_flag) { 
                    if( xSemaphore_IMU != NULL ){
                        /* See if we can obtain the semaphore.  If the semaphore is not
                           available wait 10 ticks to see if it becomes free. */
                        if( xSemaphoreTake( xSemaphore_IMU, ( TickType_t ) 10 ) == pdTRUE )
                        {
                            /* We were able to obtain the semaphore and can now access the
                               shared resource. */
                
                            /* ... */
                            send_IMU_struct();
                            /* We have finished accessing the shared resource.  Release the
                               semaphore. */
                            xSemaphoreGive( xSemaphore_IMU );
                        }
                        else
                        {
                            /* We could not obtain the semaphore and can therefore not access
                               the shared resource safely. */
                        }
                    }
                }
            } else if (input == DATA_P) {
                Serial.println("RPI input: power data request");
                if (handshake_flag) { 
                    Serial.println("Begin sending data");
                    if( xSemaphore_power != NULL ){
                        /* See if we can obtain the semaphore.  If the semaphore is not
                           available wait 10 ticks to see if it becomes free. */
                        if( xSemaphoreTake( xSemaphore_power, ( TickType_t ) 10 ) == pdTRUE )
                        {
                            /* We were able to obtain the semaphore and can now access the
                               shared resource. */
                
                            /* ... */
                            send_power_struct();
                            /* We have finished accessing the shared resource.  Release the
                               semaphore. */
                            xSemaphoreGive( xSemaphore_power );
                        }
                        else
                        {
                            /* We could not obtain the semaphore and can therefore not access
                               the shared resource safely. */
                        }
                    }
                }
            }
        }
        
        vTaskDelayUntil(&xLastWakeTime, xFrequency / portTICK_PERIOD_MS);
    }
}


void getData(int sensorNum, IMU_data* data){

    if(sensorNum == 1) {
        digitalWrite (sensor1, LOW);
        digitalWrite (sensor2, HIGH);
        digitalWrite (sensor3, HIGH);
        accelgyro.setXAccelOffset(1382);
        accelgyro.setYAccelOffset(1003);
        accelgyro.setZAccelOffset(1277);
    
        accelgyro.setXGyroOffset(121);
        accelgyro.setYGyroOffset(17);
        accelgyro.setZGyroOffset(41);
    } else if (sensorNum == 2) {
        digitalWrite (sensor1, HIGH);
        digitalWrite (sensor2, LOW);
        digitalWrite (sensor3, HIGH);
        accelgyro.setXAccelOffset(-377);
        accelgyro.setYAccelOffset(-779);
        accelgyro.setZAccelOffset(1167);
    
        accelgyro.setXGyroOffset(103);
        accelgyro.setYGyroOffset(39);
        accelgyro.setZGyroOffset(-2);
    }else if (sensorNum == 3) {
        digitalWrite (sensor1, HIGH);
        digitalWrite (sensor2, HIGH);
        digitalWrite (sensor3, LOW); 
        accelgyro.setXAccelOffset(2095);
        accelgyro.setYAccelOffset(160);
        accelgyro.setZAccelOffset(1028);
    
        accelgyro.setXGyroOffset(96);
        accelgyro.setYGyroOffset(-135);
        accelgyro.setZGyroOffset(-11);
    }

    accelgyro.getMotion6(&accelerometer_x, &accelerometer_y, &accelerometer_z, &gyro_x, &gyro_y, &gyro_z);
    
//    Wire.beginTransmission(MPU_ADDR);
//    Wire.write(0x3B);                                       // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
//    Wire.endTransmission(false);                            // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
//    Wire.requestFrom(MPU_ADDR, 6, true);                    // request a total of 6 registers
//                                                            // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
//    accelerometer_x = Wire.read()<<8 | Wire.read();         // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
//    accelerometer_y = Wire.read()<<8 | Wire.read();         // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
//    accelerometer_z = Wire.read()<<8 | Wire.read();         // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
//  
//    Wire.beginTransmission(MPU_ADDR);
//    Wire.write(0x43);                                       // starting with register 0x43 (GYRO_XOUT_H) [MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
//    Wire.endTransmission(false);                            // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
//    Wire.requestFrom(MPU_ADDR, 6, true);                    // request a total of 6 registers
//    
//    gyro_x = Wire.read()<<8 | Wire.read();                  // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
//    gyro_y = Wire.read()<<8 | Wire.read();                  // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
//    gyro_z = Wire.read()<<8 | Wire.read();                  // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
//    



    if(sensorNum == 1) {
        data->Ac1X = accelerometer_x;
        data->Ac1Y = accelerometer_y;
        data->Ac1Z = accelerometer_z;
        data->Gy1X = gyro_x;
        data->Gy1Y = gyro_y;
        data->Gy1Z = gyro_z;
    } else if (sensorNum == 2) {
        data->Ac2X = accelerometer_x;
        data->Ac2Y = accelerometer_y;
        data->Ac2Z = accelerometer_z;
        data->Gy2X = gyro_x;
        data->Gy2Y = gyro_y;
        data->Gy2Z = gyro_z;
    }else if (sensorNum == 3) {
        data->Ac3X = accelerometer_x;
        data->Ac3Y = accelerometer_y;
        data->Ac3Z = accelerometer_z;
        data->Gy3X = gyro_x;
        data->Gy3Y = gyro_y;
        data->Gy3Z = gyro_z;
    }

}


void setup() {

    delay(2000);

    Serial.begin(38400);
    Serial.println("Begin");
    Serial1.begin(38400);
    Serial.print(F("size of struct: "));
    Serial.print(IMU_data_len);
    Serial.println();
    Serial.println(F("done with setup"));

    pinMode(sensor1, OUTPUT);
    pinMode(sensor2, OUTPUT);
    pinMode(sensor3, OUTPUT);
    
//    Wire.begin();
//    Wire.beginTransmission(MPU_ADDR); // Start the transimission by communicating through the address of MPU6050
//    Wire.write(0x6B);                 // Access the PWR_MGMT_1 register to configure power mode
//    Wire.write(0);                    // Set the bit controlling SLEEP to zero (wakes up the MPU6050)
//    Wire.endTransmission(true);       // End communication

    Serial.println("Initializing I2C devices...");
    Wire.begin();
    accelgyro.initialize();
//    MPU_ARM.initialize();
//    MPU_LEG.initialize();
//    MPU_TORSO.initialize();

    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "accelgyro connection successful" : "accelgyro connection failed");
//    Serial.println(MPU_ARM.testConnection() ? "MPU_ARM connection successful" : "MPU_ARM connection failed");
//    Serial.println(MPU_LEG.testConnection() ? "MPU_LEG connection successful" : "MPU_LEG connection failed");
//    Serial.println(MPU_TORSO.testConnection() ? "MPU_TORSO connection successful" : "MPU_TORSO connection failed");

    // Initialize dummy data
    data.Ac1X = 1;
    data.Ac1Y = 2;
    data.Ac1Z = 3;
    data.Gy1X = 4;
    data.Gy1Y = 5;
    data.Gy1Z = 6;
    data.Ac2X = 7;
    data.Ac2Y = 8;
    data.Ac2Z = 9;
    data.Gy2X = 10;
    data.Gy2Y = 11;
    data.Gy2Z = 12;
    data.Ac3X = 13;
    data.Ac3Y = 14;
    data.Ac3Z = 15;
    data.Gy3X = 16;
    data.Gy3Y = 17;
    data.Gy3Z = 18;
    data.checksum = 7;

    p_data.voltage = 8;
    p_data.current = 9;
    p_data.power   = 10;
    p_data.checksum = 11;

    xSemaphore_IMU = xSemaphoreCreateBinary();
    xSemaphore_power = xSemaphoreCreateBinary();

    xSemaphoreGive(xSemaphore_IMU);
    xSemaphoreGive(xSemaphore_power);

    // Create Tasks
    xTaskCreate(handleInput, "handleInput", STACK_DEPTH, (void *) NULL, 1, NULL);
    xTaskCreate(retrievePowerData, "retrievePowerData", STACK_DEPTH, (void *) NULL, 1, NULL);
    xTaskCreate(retrieveSensorData, "retrieveSensorData", STACK_DEPTH, (void *) NULL, 1, NULL);

    vTaskStartScheduler();
}

void loop() {
}
