#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <cactus_io_DS18B20.h>
#include "ClosedCube_HDC1080.h"
ClosedCube_HDC1080 hdc1080;
int DS18B20_Pin = 2; //DS18S20 Signal pin on digital 2 
// Create DS18B20 object 
DS18B20 ds(DS18B20_Pin); 
RF24 radio(7, 8); // CE, CSN

const byte address[6] = "00001";

void setup() {
  Serial.begin(9600); // initialization of serial communication
  hdc1080.begin(0x40); // initialization of the sensor
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();

  Serial.begin(9600);
  
  
}
void loop()
{
  double tempF=hdc1080.readTemperature();
  char tempC[10];               //temporarily holds data from vals 
  String tempSVal = "";     //data on buff is copied to this string
  
  dtostrf(tempF, 4, 2, tempC);  //4 is mininum width, 4 is precision; float value is copied onto buff
  
  double humF=hdc1080.readHumidity();
  char humC[10];              
  String humSVal = "";     
  
  dtostrf(humF, 4, 2, humC);
  ds.readSensor();
  
  double wallTempF=ds.getTemperature_C();
  char wallTempC[10];
  String WalltempSVal = "";
  
  dtostrf(wallTempF, 4, 2, wallTempC);
  
  
  radio.write(&tempC, sizeof(tempC));
  radio.write(&humC, sizeof(humC));
  radio.write(&wallTempC, sizeof(wallTempC));
  delay(9000);
}

