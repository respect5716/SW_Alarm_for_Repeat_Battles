# 서머너즈워 연속전투 알림

Summoners War notification for repeat battles



## 주의사항

* 본 코드는 매크로가 아닌 단순 알람을 위해 작성되었습니다.
* 본 코드의 사용/오용/남용으로 인한 제재에 개발자는 어떠한 책임도 지지 않습니다.
* 본 코드에서는 앱 플레이어로 "녹스 플레이어"를 사용하지만 다른 플레이어를 사용하여도 무방합니다. 이때 화면 차이로 인해 코드를 일부 수정해야 할 수도 있습니다.
* 앱 플레이어가 다른 프로그램에 의해 가려져도 정상 작동합니다. 하지만 최소화할 경우 플레이 화면을 정상적으로 인식하지 못합니다.
* 본 코드에서는 알림 어플리케이션으로 "슬랙"을 사용하지만 다른 방법을 사용하여도 무방합니다. 마찬가지로 본인의 선호에 따라 알림 방식을 변경하여도 됩니다.
* "슬랙" 알림을 위해 토큰이 필요합니다. 



## 구현

1. screenshot : win32gui를 통해 녹스 플레이어 픽셀 값 추출
2. ocr : pytesseract로 전투 진행 상황 부분 문자 추출
3. send_message : '연속 전투가 종료되었습니다.' 메세지가 나오면 지정된 방식으로 메세지 발신



## Requirements

* OS : Windows 10
* Python : 3.7.3

```
## requirements.txt
numpy==1.16.4
slackclient==2.9.1
pytesseract==0.3.6
Pillow==6.1.0
```



## 실행

1. 녹스 플레이어에서 서머너즈워 실행

   <img src="asset\img_01.PNG" alt="img_01" style="zoom:33%;" />

2. 연속전투 실행 후 절전모드 클릭

   <img src="asset\img_02.PNG" alt="img_02" style="zoom:36%;" />

3. 파이썬 코드 실행

   ```
   python3 run.py
   ```