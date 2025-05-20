<<<<<<< HEAD
# CustomDiary
=======

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
git clone https://github.com/lsy216184/CustomDiary.git
```

## 6. 서버 실행
```bash
cd CustomDiary
python3 manage.py runserver
```

## 7. 사용 방법
1. 웹브라우저에서 'http://127.0.0.1:8000/ai_object_detection/' 접속

2. 회원가입을 통해 계정을 생성합니다.
   
   ![1 회원가입 화면](https://github.com/user-attachments/assets/bfc5f5ad-c38f-4f78-9788-900d7ea75a6f)
   ![2 계정생성](https://github.com/user-attachments/assets/27780c0a-ddca-41f7-a1d1-446ff5004b8e)


4. 로그인합니다.
    ![3  로그인 화면](https://github.com/user-attachments/assets/a59d1154-df69-4eec-8f13-3f8bed4219d8)



6. 글 등록하기
   •	“AI 이용하기” 버튼을 클릭해서 계시물(제목, 이미지)을 등록합니다.
    ![4  ai이용하기 버튼](https://github.com/user-attachments/assets/00a0b4e5-3604-4a3b-9e66-48dd9d510693)


  •	“파일선택”버튼을 누르면 이미지를 첨부할 수 있습니다. 
  •	“저장하기”버튼을 누르면 게시물이 등록됩니다. 

  ![5  글 등록화면](https://github.com/user-attachments/assets/74cce822-28ac-485d-8445-8bab712ba564)


5. 이미지에 AI적용하기(예측, 분류, 영역분할)
   
5-1. 이미지 예측하기 및 결과 확인
  
  •	게시물 목록 화면에서 등록한 계시물을 클릭하여 상세화면으로 이동합니다.
![6  등록게시글 확인](https://github.com/user-attachments/assets/c67c253f-af62-4e32-924e-a9188afc4858)

  •	“이미지 예측” 버튼을 눌러 이미지 예측을 실행합니다. 
    ![7  이미지 예측 버튼 클릭](https://github.com/user-attachments/assets/5e06b5b6-f550-434c-9a20-bdca6f151ce1)

  •	예측결과 이미지가 하단에 나타납니다.
  
    o	객체 클래스: 객체가 어떤 것으로 인식했는지를 나타냅니다.
    
    o	바운딩 박스: 사물의 테두리를 표시합니다. 
    
    o	확률값(%) 의미: 얼마나 정확하게 인식했는지 나타냅니다. 
    ![8  이미지 예측 결과](https://github.com/user-attachments/assets/3121db7b-893a-4350-9b86-f7eafa8544bd)

  •	“돌아가기”버튼을 클릭하면 게시물 목록 화면으로 이동가능합니다. 
    ![9 돌아가기 버튼](https://github.com/user-attachments/assets/f53a5180-94c1-4da8-8d1d-844b625a0097)

5-2. 이미지 분류하기 및 결과 확인

  •	“이미지 분류” 버튼을 눌러 이미지 분류를 실행합니다. 
  
    ![10 이미지 분류 버튼](https://github.com/user-attachments/assets/bf1ebd82-2303-4a20-8748-031061748712)

  •	분류결과가 하단에 텍스트로 표기됩니다.
  
    o	객체 클래스: 객체가 어떤 것으로 인식했는지를 나타냅니다. 
    
    o	확률값(%) 의미: 얼마나 정확하게 인식했는지 나타냅니다. 
    ![11 이미지 분류 결과](https://github.com/user-attachments/assets/b1a52a30-9cf2-4e69-acbe-8676bc978b46)
  
  •	“돌아가기”버튼을 클릭하면 게시물 목록 화면으로 이동가능합니다. 
    ![13 이미지 분류 후 돌아가기 버튼 클릭](https://github.com/user-attachments/assets/4f905556-b3d2-4ae2-83cc-dc8f74a9b58d)


5-3. 이미지 영역분할하기 및 결과 확인

  •	“이미지 영역분할” 버튼을 눌러 이미지 영역분할을 실행합니다.  
  ![13  이미지 영역분할 클릭](https://github.com/user-attachments/assets/12794002-d3f9-48d5-8d24-c8d37f7564db)

  •	분류결과 이미지가 우측에 나타납니다.
  
    o	객체 클래스 : 이미지의 각 픽셀이 어떤 클래스에 속하는지 표시합니다. 같은 클래스의 객체끼리는 같은 색으로 칠해지며, 보통 객체는 빨강으로 배경은 초록이나 파랑으로 표현됩니다.  
      ![14  이미지 영역분할 결과](https://github.com/user-attachments/assets/618b1d53-2e4d-479d-aa85-31d06e1c0011)

  
6. 글 수정, 삭제하기
  •	“수정” 버튼을 클릭하면 게시물 수정이 가능합니다. 
  •	“삭제” 버튼을 클릭하면 게시물 삭제가 가능합니다.
![15  수정 삭제 버튼](https://github.com/user-attachments/assets/f4b5ec96-c5cf-44c6-b5c9-b9360478b2f3)

>>>>>>> develop
