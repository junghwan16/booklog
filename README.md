```
.
├── apps
│   └── account
│       ├── adapters: 외부 세계(웹, DB, 메시지 버스 등)와 애플리케이션 계층을 연결하는 ‘포트 구현체’ 모음입니다.
│       │   ├── inbound: 웹 핸들러(DRF ViewSet, GraphQL resolver 등), CLI, 스케줄러 등 시스템 밖에서 안으로 들어오는 어댑터.
│       │   └── outbound: 리포지토리(ORM), 외부 API 클라이언트, 메시지 퍼블리셔 등 시스템 안에서 밖으로 나가는 어댑터.
│       ├── application: 도메인 모델을 orchestration 해주는 계층.
│       │   ├── ports: 어댑터가 구현해야 할 인터페이스 정의.
│       │   │   ├── inbound: 컨트롤러가 호출하는 포트(입력 경계).
│       │   │   └── outbound: 인프라 서비스(리포지토리·외부 API 등)가 구현해야 할 포트(출력 경계).
│       │   └── services: 유스케이스를 표현하는 서비스 객체(“계좌 개설”, “비밀번호 변경” 같은 도메인 시나리오).
│       ├── domain: 핵심 비즈니스 규칙을 담는 순수 파이썬 코드만 위치합니다.
│       └── tests
├── config
├── templates
├── manage.py
├── requirements.txt
└── README.md
```
