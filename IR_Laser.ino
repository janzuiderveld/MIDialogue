
int lowerTwoDigits, higherTwoDigits = 0;
long unsigned currentMillis, previousMillis = 0;
int sensorValue = 0;
int interval = 10;

const int controlPin[6] = {52, 50, 48, 46, 44, 42}; // define relay pins

const int triggerType = HIGH;// your relay type
int loopDelay = 1000;// delay in loop
int tmpStat =1;

// the setup routine runs once when you press reset:
void setup() {
  for(int i=0; i<6; i++)
  {
    pinMode(controlPin[i], OUTPUT);// set pin as output
    if(triggerType ==LOW){
      digitalWrite(controlPin[i], HIGH); // set initial state OFF for low trigger relay
    }else{
       digitalWrite(controlPin[i], LOW); // set initial state OFF for high trigger relay     
    }
  }
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval){
      Serial.write(255); //send the value 255 to indicate that we are sending a set of new values. The PD patch uses this to synchronize to the data.
    for(int i=0; i<6; i++)
    {
          
      sensorValue = analogRead(i);

      lowerTwoDigits =  sensorValue % 100;
      higherTwoDigits =  sensorValue / 100;
      Serial.write(lowerTwoDigits);
      Serial.write(higherTwoDigits);
  
      previousMillis = currentMillis;
    }
  }
  
  
	if(Serial.available() > 0) {
		char data = Serial.read();
		Serial.println("data");
		Serial.println(data);
	
		if(data == '9') {
      for(int i=0; i<6; i++)
      {
        channelControl(i,0,0);
      }
		}
		if(data == '0'){
      for(int i=0; i<6; i++)
      {
        channelControl(i,1,0);
      }
		}
		
		if(data == '1')
      {
        channelControl(0,0,0);
      }
		if(data == '2')
      {
        channelControl(1,0,0);
      }
		if(data == '3')
      {
        channelControl(2,0,0);
      }
		if(data == '4')
      {
        channelControl(3,0,0);
      }
		if(data == '5')
      {
        channelControl(4,0,0);
      }
		if(data == '6')
      {
        channelControl(5,0,0);
      }
	}
}

void channelControl(int relayChannel, int action, int t)
{
  int state =LOW;
  String statTXT =" ON";
  if(triggerType == LOW)
  {    
    if (action ==0)// if OFF requested
    {
      state = HIGH;
      statTXT = " OFF";
    }
    digitalWrite(controlPin[relayChannel], state);
    if(t >0 )
    {
      delay(t);
    }
       Serial.print ("Channel: ");
       Serial.print(relayChannel); 
       Serial.print(statTXT);
       Serial.print(" - "); 
       Serial.println(t);        
  }else{
    if (action ==1)// if ON requested
    {
      state = HIGH;     
    }else{
      statTXT = " OFF";    
    }
    digitalWrite(controlPin[relayChannel], state);
    if(t >0 )
    {
      delay(t);
    }
       Serial.print ("Channel: ");
       Serial.print(relayChannel); 
       Serial.print(statTXT);
       Serial.print(" - "); 
       Serial.println(t);    
  }

}
