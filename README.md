
# YOLO Object Detection App

## 프로젝트 소개
yolo object detection app은 Django 기반의 웹 애플리케이션으로, 사용자가 업로드한 이미지를 YOLOv11 모델을 이용해 객체를 검출하는 프로그램입니다.

## 기술 스택
- Python 3.x
- Django
- YOLOv11 (Ultralytics)
- Docker
- HTML/CSS

##  설치 및 실행 방법

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
1.웹브라우저에서 'http://127.0.0.1:8000/ai_object_detection/' 접속

2. 회원가입을 통해 계정을 생성합니다. 
![회원가입](https://github.com/user-attachments/assets/e831227c-4a6d-49fd-b7ff-da5af94e7703)
![계정생성](https://github.com/user-attachments/assets/a2d3ae35-9f6c-40f8-88e8-f5eddca6b666)

3. 로그인합니다.  
![로그인 화면](https://github.com/user-attachments/assets/c3716cde-e81d-4e69-921e-0d5800e58e98)

4. 글 등록하기
  •	“AI 이용하기” 버튼을 클릭해서 계시물(제목, 이미지)을 등록합니다.
![게시물 등록](https://github.com/user-attachments/assets/9f077da7-1722-48f8-af88-83b84f0d91b1)

  •	“파일선택”버튼을 누르면 이미지를 첨부할 수 있습니다. 
  •	“저장하기”버튼을 누르면 게시물이 등록됩니다.
![제목, 이미지 첨부](https://github.com/user-attachments/assets/ec2b3050-45ca-4434-8e48-72376d129dbb)


5. 이미지 예측하기 및 결과 확인
  •	게시물 목록 화면에서 등록한 계시물을 클릭하여 상세화면으로 이동합니다.
![등록 게시물 확인](https://github.com/user-attachments/assets/a2eb45eb-867b-4df0-b815-d5b13ee553a4)

  •	“YOLO 예측하기” 버튼을 눌러 이미지 예측을 실행합니다.
  •	“수정” 버튼을 클릭하면 게시물 수정이 가능합니다. 
  •	“삭제” 버튼을 클릭하면 게시물 삭제가 가능합니다.
![yolo 예측하기](https://github.com/user-attachments/assets/04cc2c8c-ed80-4b39-9410-7f3546e96873)

  •	예측결과 이미지가 하단에 나타납니다.
    o	객체 클래스: 객체가 어떤 것으로 인식했는지를 나타냅니다.
    o	바운딩 박스: 사물의 테두리를 표시합니다. 
    o	확률값(%) 의미: 얼마나 정확하게 인식했는지 나타냅니다.
  •	“돌아가기”버튼을 클릭하면 게시물 목록 화면으로 이동가능합니다.
![예측결과 확인](https://github.com/user-attachments/assets/05a6858c-3056-440e-95f4-0f73f0aa499f)

