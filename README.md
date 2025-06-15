# 북로그 (Booklog) - 클린 아키텍처 기반 Django 프로젝트

이 프로젝트는 독서 활동을 기록하고 관리하는 웹 애플리케이션입니다.  
**클린 아키텍처(Clean Architecture)** 설계를 적용하여, 유지보수가 용이하고 테스트하기 쉬운 구조를 목표로 합니다.

## ✨ 기술 스택

- **백엔드**: Python, Django
- **아키텍처**: 클린 아키텍처 (Hexagonal / Ports & Adapters)
- **테스트**: Pytest, pytest-django

## 🏛️ 아키텍처 개요

프로젝트는 계층화된 아키텍처를 따르며, 각 계층의 역할은 다음과 같습니다.

- **`domain`**: 핵심 비즈니스 규칙과 엔티티를 정의하는 순수한 Python 코드 계층입니다. 프레임워크에 대한 의존성이 없습니다.
- **`application`**: 애플리케이션의 유스케이스(Use Case)를 정의합니다. 도메인 계층을 조합하여 비즈니스 흐름을 구현합니다.
- **`adapters`**: 외부 세계와의 인터페이스를 담당합니다. Django 웹 뷰, 데이터베이스(ORM), 이메일 전송 등 외부 기술과의 연동을 처리합니다.

이러한 구조를 통해 비즈니스 로직과 외부 인프라를 분리하여 유연하고 확장 가능한 애플리케이션을 만듭니다.

## 🚀 로컬 환경에서 실행하기

1. **가상 환경 생성 및 활성화**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   (Windows의 경우: `.venv\Scripts\activate`)

2. **의존성 설치**:

   ```bash
   pip install -r requirements.txt
   ```

   > `requirements.txt` 파일이 아직 없다면, 주요 라이브러리를 직접 설치하세요.
   > `pip install django pytest pytest-django`

3. **데이터베이스 마이그레이션**:

   ```bash
   python manage.py migrate
   ```

4. **개발 서버 실행**:
   ```bash
   python manage.py runserver
   ```

서버 실행 후, 웹 브라우저에서 `http://127.0.0.1:8000` 주소로 접속할 수 있습니다.

## ✅ 테스트 실행하기

프로젝트의 모든 테스트를 실행하려면 다음 명령어를 입력하세요.

```bash
pytest
```
