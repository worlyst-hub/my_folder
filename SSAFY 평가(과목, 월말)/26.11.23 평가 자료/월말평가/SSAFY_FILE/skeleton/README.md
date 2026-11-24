# Booklog API

Django REST Framework 기반의 독서 기록(도서·댓글) REST API 프로젝트입니다.

---

## 프로젝트 실행 방법

### 1. 가상환경 생성 및 패키지 설치

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 개발 서버 실행

주어진 `db.sqlite3` 에 테이블과 초기 데이터가 모두 들어 있으므로 migrate 와 loaddata 는 필요하지 않습니다.

```bash
python manage.py runserver
```

서버가 실행되면 `http://127.0.0.1:8000/` 에서 API를 사용할 수 있습니다.

### (참고) 데이터베이스를 초기 상태로 되돌리고 싶은 경우

```bash
# db.sqlite3 파일을 삭제한 뒤
python manage.py migrate
python manage.py loaddata books.json comments.json
```

---

## 전체 API 엔드포인트 목록

모든 URL은 `/api/v1/` 로 시작하며, **끝에 `/` 를 붙여** 요청합니다.

### 도서 (Books)

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/v1/books/` | 도서 목록 조회 |
| POST | `/api/v1/books/` | 도서 생성 |
| GET | `/api/v1/books/<book_pk>/` | 도서 상세 조회 (댓글 목록 포함) |
| PUT | `/api/v1/books/<book_pk>/` | 도서 수정 |
| DELETE | `/api/v1/books/<book_pk>/` | 도서 삭제 |

### 댓글 (Comments)

| Method | URL | 설명 |
|--------|-----|------|
| GET | `/api/v1/comments/` | 전체 댓글 목록 조회 |
| GET | `/api/v1/comments/<comment_pk>/` | 댓글 단건 조회 |
| PUT | `/api/v1/comments/<comment_pk>/` | 댓글 수정 |
| DELETE | `/api/v1/comments/<comment_pk>/` | 댓글 삭제 |
| POST | `/api/v1/books/<book_pk>/comments/` | 특정 도서에 댓글 작성 |

### API 문서 (참고)

| URL | 설명 |
|-----|------|
| `/api/schema/swagger-ui/` | Swagger UI |
| `/api/schema/redoc/` | ReDoc |

---

## 모델 구조

| 모델 | 필드 |
|------|------|
| Book | id, title(도서 제목), author(저자), content(내용), finished(완독 여부), created_at, updated_at |
| Comment | id, book(FK -> Book), content(댓글 내용), created_at, updated_at |

- Book : Comment = 1 : N
- Comment 모델의 `book` 필드에는 `related_name` 이 지정되어 있지 않습니다.
- `models.py` 는 수정하지 않습니다. 수정 시 주어진 `db.sqlite3` 와 맞지 않아 서버가 정상 동작하지 않을 수 있습니다.

## Fixtures 데이터 구성

| 모델 | 수량 |
|------|------|
| Book | 5개 |
| Comment | 6개 |

## 프로젝트 구조

```
skeleton/
├── booklog_pjt/          # 프로젝트 설정 (settings.py, urls.py)
├── books/
│   ├── fixtures/         # 초기 데이터 (books.json, comments.json)
│   ├── models.py         # Book, Comment 모델
│   ├── serializers.py    # 직렬화 클래스
│   ├── urls.py           # books 앱 URL
│   └── views.py          # API view 함수
├── db.sqlite3            # 초기 데이터가 들어 있는 DB
├── problem_10_11.md      # 서술형 답안 작성 파일
├── manage.py
└── requirements.txt
```
