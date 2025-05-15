  int led1=10;
  int led2=5;
  int sw1=3;
  int flag=0;
void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(sw1, INPUT);

  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
int push1=digitalRead(sw1);
if(push1==1 && flag==0)
{
  digitalWrite(led1, HIGH);
  delay(1000);
  digitalWrite(led2, LOW);
delay(1000);
  flag++;
}
else if (push1==1 && flag==1)
{
  digitalWrite(led1, LOW);
  delay(1000);
  digitalWrite(led2, HIGH);
  delay(1000);
  flag++;
}
else if(push1==1 && flag==2)
{
  digitalWrite(led1, HIGH);
  delay(1000);
  digitalWrite(led2, HIGH);

  delay(1000);
  flag++;
}
else if(push1==1 && flag==3)
{
  digitalWrite(led1, LOW);
  delay(1000);
  digitalWrite(led2, LOW);
  delay(1000);
  flag=0;
}

}
