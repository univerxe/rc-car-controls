int IN1 = 6;
int IN2 = 7;
int IN3 = 8;
int IN4 = 9;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  forward();
  delay(1000);
  stop();
}

void forward(){
  digitalWrite(IN2, LOW);
  digitalWrite(IN4, LOW);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN3, HIGH);
}

void backward(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN4, HIGH);
}

void left() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN4, HIGH);
}

void right() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN4, LOW);
}

void stop(){
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}


void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming byte

    switch (command) {
      case 'W':
        forward();
        break;
      case 'S':
        backward();
        break;
      case 'A':
        left();
        break;
      case 'D':
        right();
        break;
      case 'O':
        stop();
        break;

      default:
        stop(); // Stop if any other key is pressed
        break;
    }
  }
}
