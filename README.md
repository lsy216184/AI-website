# imageAI

### 프로젝트 소개
imageAI는 Django 기반의 웹 애플리케이션으로, 사용자가 업로드한 이미지를 3가지 AI모델(YOLO11, Vision Transformer, DeepLabV3 + ResNet101)을 적용시켜 결과물을 보여주는 프로그램입니다.

### 기술 스택
**Backend FrameWork**
- Python 3.x
- Django

**Models**
- YOLOv11 (Ultralytics)
- Vision Transformer (timm)
- DeepLabV3 + ResNet101 (torchvision)

**Containerization**
- Docker

**Frontend**
- HTML/CSS

###  설치 및 실행 방법

## 1. 사용할 Docker 이미지 다운로드
```bash
docker pull ultralytics/ultralytics
```

## 2. Docker 컨테이너 생성
```bash
docker run -it \
  --name django_server \
  --privileged \
  --gpus all \
  --network host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /etc/localtime:/etc/localtime:ro \
  -e TZ=Asia/Seoul \
  -v /dev:/dev \
  -w /root \
  ultralytics/ultralytics:latest
```

## 3. Docker 컨테이너 접속
```bash
docker exec -it django_server bash
```

## 4. 컨테이너 내부에 Django 설치
```bash
pip install django
```

## 5. 프로젝트 클론
```bash
git clone https://github.com/lsy216184/AI-website.git
```

## 6. 서버 실행
```bash
cd CustomDiary
python3 manage.py runserver
```

## 7. 사용 방법

1. 웹브라우저에서 'http://127.0.0.1:8000/' 접속
   •	페이지의 ‘고급’을 클릭합니다.
   •	‘222.109.41.89(안전하지 않음)’을 클릭합니다.
![881비공개 연결이 아님](https://github.com/user-attachments/assets/d53c4b5a-e199-40b6-a274-bdf5b59dbfa6)
![882 비공개 안전하지 않음](https://github.com/user-attachments/assets/ef089e26-7e5c-4489-9a36-88976514dd74)



2. 회원가입을 통해 계정을 생성합니다.
   
   ![883 회원가입](https://github.com/user-attachments/assets/60d2de37-c7ed-4f3c-be21-e49681ca7ffe)
   ![884 계정생성](https://github.com/user-attachments/assets/30b4b7dc-739d-468e-906b-bf85a6bb71b2)




3. 로그인합니다.
   
   ![885 로그인](https://github.com/user-attachments/assets/50d4833d-c3bd-46dd-8bed-6b5c165d4cf3)





4. 글 등록하기
   
   •	“AI 이용하기” 버튼을 클릭해서 계시물(제목, 이미지)을 등록합니다.
   
   ![886 글등록](https://github.com/user-attachments/assets/04246923-8c29-4615-83e8-bec371dfc0cf)



   •	“파일선택”버튼을 누르면 이미지를 첨부할 수 있습니다. 
  
   •	“저장하기”버튼을 누르면 게시물이 등록됩니다.

   ![887 제목, 이미지 등록](https://github.com/user-attachments/assets/d5708c58-8f74-4972-b637-df676a25c43a)






6. 이미지에 AI적용하기(예측, 분류, 영역분할)

    5_1.이미지 예측하기 및 결과 확인
  
    •	게시물 목록 화면에서 등록한 계시물을 클릭하여 상세화면으로 이동합니다.

    ![888 등록게시물 확인](https://github.com/user-attachments/assets/d1f90574-915b-4165-a588-e71fd233f7c1)



    •	“이미지 예측” 버튼을 눌러 이미지 예측을 실행합니다. 

    ![889 예측버튼 클릭](https://github.com/user-attachments/assets/0e92524e-2007-4f97-89ef-f562d5f54d9b)



    •	예측결과 이미지가 하단에 나타납니다.
      - 객체 클래스: 객체가 어떤 것으로 인식했는지를 나타냅니다.
      - 바운딩 박스: 사물의 테두리를 표시합니다. 
      - 확률값(%) 의미: 얼마나 정확하게 인식했는지 나타냅니다. 
  
    ![900 이미지예측결과](https://github.com/user-attachments/assets/345b55da-3053-4761-8222-416265249d70)


    •	“돌아가기”버튼을 클릭하면 게시물 목록 화면으로 이동가능합니다. 

    


    





    5-2. 이미지 분류하기 및 결과 확인

    •	“이미지 분류” 버튼을 눌러 이미지 분류를 실행합니다.
   
     ![901 이미지 부뉴 버튼 클릭](https://github.com/user-attachments/assets/7aab20e9-487a-4bf5-b100-9cf3c69eb1c3)

  
    •	분류결과가 하단에 텍스트로 표기됩니다.
    
      -	객체 클래스: 객체가 어떤 것으로 인식했는지를 나타냅니다. 
      
      -	확률값(%) 의미: 얼마나 정확하게 인식했는지 나타냅니다. 
      
      ![902 이미지 분류 결과](https://github.com/user-attachments/assets/edb0f78e-dd1c-428e-a508-1d0ca01c458e)

    
    •	“돌아가기”버튼을 클릭하면 게시물 목록 화면으로 이동가능합니다. 
    
      
  




     
    5-3. 이미지 영역분할하기 및 결과 확인
  
    •	“이미지 영역분할” 버튼을 눌러 이미지 영역분할을 실행합니다.  
    
      ![903 이미지 영역분할](https://github.com/user-attachments/assets/04513d26-9922-4e50-97cb-085467ddd9e4)

  
    •	분류결과 이미지가 우측에 나타납니다.
    
      - 객체 클래스 : 이미지의 각 픽셀이 어떤 클래스에 속하는지 표시합니다. 같은 클래스의 객체끼리는 같은 색으로 칠해지며, 보통 객체는 빨강으로 배경은 초록이나 파랑으로 표현됩니다.  
      ![904 이미지 영역분할 결과](https://github.com/user-attachments/assets/b20e42dd-0456-4df5-86fa-c3270ce72af2)

      

    
    
6. 글 수정, 삭제하기
     
    •	“수정” 버튼을 클릭하면 게시물 수정이 가능합니다.
  
    •	“삭제” 버튼을 클릭하면 게시물 삭제가 가능합니다.
    
      ![905 이미지 수정,삭제](https://github.com/user-attachments/assets/9294c113-7134-42ca-9432-195817b911ba)


