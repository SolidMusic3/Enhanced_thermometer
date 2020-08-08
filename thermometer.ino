
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

#define BMP280_ADRESA (0x76)
Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);

  if (!bmp.begin(BMP280_ADRESA)) {
    while (1);
  }
}

byte cpu = 0;
byte gpu = 0;

void loop() {

  int teplota = int(bmp.readTemperature());
  lcd.setCursor(5,0);
  lcd.print((char)124);
  lcd.print("out ");
  lcd.print((char)124);
  lcd.setCursor(5,1);
  lcd.print((char)124);
  lcd.print(teplota);
  lcd.print((char)223);
  lcd.print("C");
  lcd.print((char)124);
  
  if (Serial.available()){
    gpu = Serial.read();
    cpu = Serial.read();
    
    lcd.setCursor(0,0);
    lcd.print("cpu ");
    lcd.setCursor(0,1);
    lcd.print(cpu);
    lcd.print((char)223);
    lcd.print("C");

    lcd.setCursor(12,0);
    lcd.print("gpu ");
    lcd.setCursor(12,1);
    lcd.print(gpu);
    lcd.print((char)223);
    lcd.print("C");
    Serial.println("b");
  }else{
    lcd.setCursor(0,0);
    lcd.print("    ");
    lcd.setCursor(0,1);
    lcd.print("    ");
    lcd.setCursor(12,0);
    lcd.print("    ");
    lcd.setCursor(12,1);
    lcd.print("    ");
    Serial.println("b");
  }

  delay(1000);
}
