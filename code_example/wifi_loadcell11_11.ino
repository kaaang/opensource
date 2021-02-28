#include "HX711.h"

// HX711 circuit wiring
#define LOADCELL_DOUT_PIN         2
#define LOADCELL_SCK_PIN          3

#include <SoftwareSerial.h> 

// scale - 10Kg loadcell : 226 / 5kg loadcell : 372
// ADC 모듈에서 측정된 결과값을 (loadcellValue)값 당 1g으로 변환해 줌
float loadcellValue = 457.0;

HX711 scale;

SoftwareSerial mySerial(4,5); //RX,TX 

String ssid = "Nowiz"; 
String PASSWORD = "pass@word"; 
String host = "내 컴퓨터 아이피"; 
String quit ="AT+CWQAP";

void connectWifi(){
  //String join ="AT+CWJAP=\"" + ssid + "\",\"" + PASSWORD + "\"";

  String join ="AT+CWJAP=\"Nowiz\",\"pass@word\"";  
  Serial.println("Connect Wifi...");
  //Serial.println(join);
  mySerial.println(join);
  delay(10000); 
  if(mySerial.find("WIFI CONNECTED")) 
  { 
    Serial.print("WIFI connect\n"); 
  }
  else 
  { 
    Serial.println("connect timeout\n");
    mySerial.println(quit);
  }
  delay(1000); 
} 

void httpclient(String char_input){ 
  delay(100); 
  Serial.println("connect TCP..."); 
  mySerial.println("AT+CIPSTART=\"TCP\",\""+host+"\",8787"); 
  delay(500); 
  if(Serial.find("ERROR")) return; 
  
  Serial.println("Send data..."); 
  String url=char_input; 
  String cmd="GET /process.php?temp="+url+" HTTP/1.0\r\n\r\n"; 
  mySerial.print("AT+CIPSEND="); 
  mySerial.println(cmd.length()); 
  Serial.print("AT+CIPSEND="); 
  Serial.println(cmd.length()); 
  
  if(mySerial.find(">")) 
  { 
    Serial.print(">"); 
  }else { 
    mySerial.println("AT+CIPCLOSE"); 
    Serial.println("connect timeout"); 
    
    delay(1000); 
    return; 
  } 
  delay(500); 
  
  mySerial.println(cmd); 
  Serial.println(cmd); 
  delay(100); 
  if(Serial.find("ERROR")) return; 
  mySerial.println("AT+CIPCLOSE"); 
  delay(100); 
}

void setup() {
  // put your setup code here, to run once:
 
  Serial.begin(9600); 
  mySerial.begin(9600); 
  
  // 로드셀 HX711 보드 pin 설정
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  // 부팅 후 잠시 대기 (2초)
  delay(2000);

  // 측정값 1회 읽어오기
  Serial.print("read: \t\t\t");
  Serial.println(scale.read());

  delay(1000);

  // 스케일 설정
  scale.set_scale(loadcellValue);
  
  // 오프셋 설정(10회 측정 후 평균값 적용) - 저울 위에 아무것도 없는 상태를 0g으로 정하는 기준점 설정(저울 위에 아무것도 올려두지 않은 상태여야 합니다.)   
  scale.tare(10);    

  // 설정된 오프셋 및 스케일 값 확인
  Serial.print("Offset value :\t\t");
  Serial.println(scale.get_offset());
  Serial.print("Scale value :\t\t");
  Serial.println(scale.get_scale());

  // (read - offset) 값 확인 (scale 미적용)
  Serial.print("(read - offset) value: \t");  
  Serial.println(scale.get_value());

  delay(2000);
  
  connectWifi();
  //mySerial.println(quit); 
  delay(500);
}

void loop() {
  // 오프셋 및 스케일이 적용된 측정값 출력 (5회 측정 평균값) 
  //Serial.print("value :\t");
  //Serial.print(-1 * scale.get_units(5), 2);    // 5회 측정 평균값, 소수점 아래 2자리 출력
  //Serial.println(" g");

    // 오프셋 및 스케일이 적용된 측정값 출력 (5회 측정 평균값) 
  Serial.println("Go");
  Serial.print("value :\t");
  double lastvalue = -1 * scale.get_units(5);
  
  int timecount = 0;
  
  Serial.print(lastvalue,2);    // 5회 측정 평균값, 소수점 아래 2자리 출력
  Serial.println(" g");
    
  // 30초 대기
  delay(3000);
  
  double newvalue = -1 * scale.get_units(5);
  Serial.print(newvalue, 2);
  Serial.println("g");
  if (newvalue - lastvalue >= 50 || newvalue - lastvalue <= -50) // 50ml 이상 차이 감지
  {
    Serial.println("물 변화 감지");
    if (newvalue - lastvalue <= -50) // 물 양이 줄었을 경우
      timecount = 0;
      // 목표음수량까지 남은 수치 감소시키는 함수 필요
  }
  else // 물 양 변화 없으면 경과시간 증가 및 갱신
  {
    timecount++;
    lastvalue = newvalue; // 물의 양 갱신
  }

  if (timecount > 7200) // 물 양 변화없이 7200초 경과
  {
    Serial.println("물 마신지 2시간 경과");
  }
  
  //String str_output = String(temp)+"&weight="+String(weight); 
  //delay(1000); 
  
  //httpclient(str_output); 
  //delay(1000); 
  
  //Serial.find("+IPD"); 
  while (mySerial.available()) 
  {
    char response = mySerial.read();
    Serial.write(response);
    if(response=='\r') Serial.print('\n'); 
  }
  Serial.println("\n==================================\n");
  delay(2000);
}
