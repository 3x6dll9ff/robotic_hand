#include <Servo.h>

Servo Servo1;  // Создаем объект для сервомотора

int servoPin = 9;  // Пин для сервомотора
int angle = 0;     // Переменная для хранения угла сервомотора

void setup() {
  Serial.begin(9600);  // Инициализация последовательного порта с baud rate 9600
  Servo1.attach(servoPin);  // Подключаем сервомотор
}

void loop() {
  if (Serial.available() > 0) {
    angle = Serial.parseInt();  // Получаем угол из последовательного порта

    // Отладочная печать, чтобы увидеть данные
    Serial.print("Received angle: ");
    Serial.println(angle);

    if (angle >= 0 && angle <= 180) {
      Servo1.write(angle);  // Поворачиваем сервомотор в заданный угол
      Serial.print("Servo Angle: ");
      Serial.println(angle);  // Отправляем угол обратно в монитор порта для отладки
    }
  }
}
