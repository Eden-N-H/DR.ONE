const int trigPin = 3;
const int echoPin = 2;
const int led = 5;

float duration, distance;

void setup()
{
  pinMode(led, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration*.0343)/2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println("cm");

  delay(100);

  if (distance <= 20) {
    digitalWrite(led, HIGH);
    delay(100);
  } else {
    digitalWrite(led, LOW);
    delay(100);
  }
}
