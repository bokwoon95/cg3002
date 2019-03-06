#include <Arduino_FreeRTOS.h>
#include <semphr.h>  // add the FreeRTOS functions for Semaphores (or Flags).
#include <Wire.h>

#define STACK_DEPTH 128

// https://arduino.stackexchange.com/questions/9899/serial-structure-data-transfer-between-an-arduino-and-a-linux-pc
struct __attribute__ ((packed)) IMU_data {
    int16_t AcX;          
    int16_t AcY;
    int16_t AcZ;
    int16_t GyX;
    int16_t GyY;
    int16_t GyZ;
}; 

SemaphoreHandle_t xSemaphore = NULL;

// instantiate one struct
struct IMU_data data;

// length of the structure
int IMU_data_len = sizeof(IMU_data);

// send the structure giving the IMU state through serial
void send_IMU_struct() {
    Serial.println("Sending: S");
    Serial1.write('S');
    Serial.println("Sending: E");
    Serial1.write((uint8_t *)&data, IMU_data_len);
    Serial1.write('E');
    return;

}

int handshake_flag = 0;

byte ACK = 0;
byte SYN = 1;
byte SYN_ACK = 2;
byte DATA_R = 3;
byte DATA_S = 4;

/**
 * Retrieve data from sensors
 */
void retrieveSensorData(void *p){
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = 16;

    for(;;) {
        if( xSemaphore != NULL ){
            /* See if we can obtain the semaphore.  If the semaphore is not
               available wait 10 ticks to see if it becomes free. */
            if( xSemaphoreTake( xSemaphore, ( TickType_t ) 10 ) == pdTRUE )
            {
                /* We were able to obtain the semaphore and can now access the
                   shared resource. */

                /* ... */

                /* We have finished accessing the shared resource.  Release the
                   semaphore. */
                xSemaphoreGive( xSemaphore );
            }
            else
            {
                /* We could not obtain the semaphore and can therefore not access
                   the shared resource safely. */
            }
        }
    }

    vTaskDelayUntil(&xLastWakeTime, xFrequency / portTICK_PERIOD_MS);

}

/**
 * Retrieve data from power management system
 */
void retrievePowerData(void *p){
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = 128;

    for(;;){
        if( xSemaphore != NULL ){
            /* See if we can obtain the semaphore.  If the semaphore is not
               available wait 10 ticks to see if it becomes free. */
            if( xSemaphoreTake( xSemaphore, ( TickType_t ) 10 ) == pdTRUE )
            {
                /* We were able to obtain the semaphore and can now access the
                   shared resource. */

                /* ... */

                /* We have finished accessing the shared resource.  Release the
                   semaphore. */
                xSemaphoreGive( xSemaphore );
            }
            else
            {
                /* We could not obtain the semaphore and can therefore not access
                   the shared resource safely. */
            }
        }
    }

    vTaskDelayUntil(&xLastWakeTime, xFrequency / portTICK_PERIOD_MS);

}

int response = 0;

void handle_handshake(int skip) {

    while (handshake_flag == 0) {
        if (skip) { // we already received SYN
            Serial1.print(SYN-ACK);
            skip = 0;
        } else if (Serial1.available()) {
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
    Serial.println("Handling input");
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = 16;
    int input;
    for(;;){
        if (Serial1.available()) { // if is an available byte..
            input = Serial1.read();  // read it
            if (input == SYN) {      // RPI is trying to initiate handshake
                Serial.println("RPI input: handshake");
                handshake_flag = 0;
                handle_handshake(1);
            } else if (input == DATA_R) { // RPI is requesting data
                Serial.println("RPI input: data request");
                if (handshake_flag) { 
                    Serial.println("Begin sending data");
                    send_IMU_struct();
                } else {
                  //TODO
                }
            }
        }
    }

    vTaskDelayUntil(&xLastWakeTime, xFrequency / portTICK_PERIOD_MS);

}

void setup() {

    delay(2000);

    Serial.begin(115200);
    Serial.println("Begin");
    Serial1.begin(115200);
    Serial.print(F("size of struct: "));
    Serial.print(IMU_data_len);
    Serial.println();
    Serial.println(F("done with setup"));

    // Initialize dummy data
    data.AcX = 1;
    data.AcY = 2;
    data.AcZ = 3;
    data.GyX = 4;
    data.GyY = 5;
    data.GyZ = 6;

    xSemaphore = xSemaphoreCreateBinary();

    xSemaphoreGive(xSemaphore);

    // Create Tasks
    xTaskCreate(handleInput, "handleInput", STACK_DEPTH, (void *) NULL, 0, NULL);
    //  xTaskCreate(retrievePowerData, "retrievePowerData", STACK_DEPTH, (void *) NULL, 1, NULL);
    //  xTaskCreate(retrieveSensorData, "retrieveSensorData", STACK_DEPTH, (void *) NULL, 1, NULL);

    vTaskStartScheduler();


}

void loop() {
}
