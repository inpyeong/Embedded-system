#include wiringPi.h
#include stdio.h
#include systime.h
#include stdint.h
#include time.h
#include signal.h
#include string.h

#define Trig    0
#define Echo    1

float dis;
float beforeDis;
int timeCheck;
int printCheck;
int cnt = 0;
uint32_t allTime;

void ultraInit(void)
{
    pinMode(Echo, INPUT);
    pinMode(Trig, OUTPUT);
}

void printScreen() {
   cnt++;

   if (printCheck == 0) 
       printf(%d %0.2f cmn, cnt, dis);
   else if (printCheck == 1) 
       printf(%d %0.2f cm  NRn, cnt, beforeDis);
   else if (printCheck == 2) 
       printf(%d %0.2f cm  TOn, cnt, beforeDis);
}

void trigger() 
{
   digitalWrite(Trig, LOW);
   delayMicroseconds(2);

   digitalWrite(Trig, HIGH);
   delayMicroseconds(10);
   digitalWrite(Trig, LOW);
}

void myInterrupt(void) 
{
   struct timeval tv1;
   struct timeval tv2;
   long time1, time2;
   uint32_t sig1T, sig2T;

   sig1T = millis();
   while(!(digitalRead(Echo) == 1));

   gettimeofday(&tv1, NULL);

   while(!(digitalRead(Echo) == 0))
        sig2T = millis();

   gettimeofday(&tv2, NULL);

   time1 = tv1.tv_sec  1000000 + tv1.tv_usec;
   time2 = tv2.tv_sec  1000000 + tv2.tv_usec;

   if (sig2T - sig1T = 30) 
        printCheck = 2;

   dis = (float)(time2 - time1)  1000000  34000  2;
   beforeDis = dis; 
}

int main(void)
{
  if(wiringPiSetup() == -1){ when initialize wiring failed,print messageto screen
        printf(setup wiringPi failed !);
        return 1;
  }

ultraInit();

if (wiringPiISR(Echo, INT_EDGE_RISING, &myInterrupt)  0) 
    {
        printf(setup ISR failed !);
        return 1;
    }

    while (1) {
        uint32_t timeTemp;
        allTime = millis();  
        if (allTime % 50 == 0 && !timeCheck) { 
            timeTemp = allTime;  
            timeCheck = 1;

            if (allTime  60000) {  
                return 0;
            }
            if (digitalRead(Echo) == 1) {  
                printCheck = 1;

                printScreen();
                continue;
            }

            trigger();
            printScreen();
        }
        if (timeCheck == 1 && timeTemp != allTime) {  
            timeCheck = 0;
            printCheck = 0;
        }
   }
}
