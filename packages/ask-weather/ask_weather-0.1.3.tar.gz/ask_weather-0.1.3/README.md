# 날씨 정보 제공 패키지

## 목적
이 패키지는 사용자가 `OpenWeatherMap API`의 일기예보 정보를 간편하게 조회할 수 있도록 돕기 위해 개발되었습니다. 

## 사용하기
이 패키지는 Python 3.11에서 동작을 확인했습니다.

1. [openweathermap api key](https://openweathermap.org/api) 발급
2. openai api key 발급
3. 프로젝트 루트 혹은 특정 위치에 .env 파일 생성
```
OPENWEATHERMAP_API_KEY=""
OPENAI_API_KEY=""
```
# 프로젝트 루트에 .env 파일이 위치하지 않을 경우 env_path를 입력해서 아래 환경변수 호출
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)

from ask_weather.agent import WeatherAgent

# WeatherAgent 인스턴스 생성
agent = WeatherAgent()

# 위치와 날짜에 대한 질의
location = "Seoul"
date = "2024-10-15"
query = f"{date}의 {location} 날씨가 궁금해요."
result = agent.query(query)
print(result)
```

### 패키지 설치
```bash
# Poetry로 패키지 설치
poetry install
# poetry env use python3.11
```

### 테스트하기
```
poetry run pytest
```

### package 만들기
1. [pypi](https://pypi.org/) 회원가입 후 api key 발급
2. `poetry config pypi-token.pypi api_key` 실행
3. `poetry build`로 whl 파일 생성
4. `poetry publish --build`로 프로젝트 배포

### reference
이 프로젝트는 [위키독스 LangChain 가이드](https://wikidocs.net/261571)를 참고했습니다.