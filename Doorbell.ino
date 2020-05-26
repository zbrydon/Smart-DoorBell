// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_TSL2561_U.h>


int led = D6;
int com = D4;
int com2 =D3;
int light; 
int val = 0; 
int val2 = 0;

bool InLight = false;
bool OutLight = false;


Adafruit_TSL2561_Unified tsl = Adafruit_TSL2561_Unified(TSL2561_ADDR_FLOAT, 12345);

void configureSensor(void)
{
  tsl.enableAutoRange(true);            
  tsl.setIntegrationTime(TSL2561_INTEGRATIONTIME_13MS);     
}

void readLight()
{
    /* Get a new sensor event */ 
  sensors_event_t event;
  tsl.getEvent(&event);
 
  /* Display the results (light is measured in lux) */
  if (event.light)
  {
    light = event.light;
    val = digitalRead(com);
    val2 = digitalRead(com2);
    //Particle.publish("ProximityTest", String(val));
    //Particle.publish("MotionTest", String(val2));
    //Particle.publish("VOltage test", String(com2));
    if (val == 1 && val2 == 1)
    {
        Particle.publish("Proximity", String(val));
        Particle.publish("Motion", String(val2));
        Particle.publish("Alert", String(val + val2));
        
    }
    else if(val == 1 && val2 ==0)
    {
        Particle.publish("Possible Package",String(val));
        
    }
    else if(val == 0 && val2 == 1)
    {
        Particle.publish("Motion Further Away", String(val2));
        
    }
    
    
    if (light > 100 && !InLight || val2 == 0)
    {
        
        InLight = true;
        
        digitalWrite(led, LOW);  // sets the LED to the button's value
        Particle.publish("Light", "Bright");
        OutLight = false; 
    }
    else if (light < 50 && !OutLight && val2 == 1)
    {
        OutLight = true;
           // read the input pin
        digitalWrite(led, HIGH);  // sets the LED to the button's value
        Particle.publish("Light", "Dim");
       
        InLight = false;
    }

  }
  else
  {
    /* If event.light = 0 lux the sensor is probably saturated
       and no reliable data could be generated! */
    Particle.publish("Sensor overload");
  }
  delay(300000);
}


void setup(){
  Serial.begin(9600);
  Particle.publish("Test");
  pinMode(led, OUTPUT);
  pinMode(com, INPUT);
  pinMode(com2, INPUT);
  /* Initialise the sensor */
  if(!tsl.begin())
  {
    /* There was a problem detecting the ADXL345 ... check your connections */
    Particle.publish("Ooops, no TSL2561 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  configureSensor();
}

void loop(){
  readLight();
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
}