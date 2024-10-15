import os
import requests
from datetime import datetime, timedelta
from langchain_core.tools import tool
from dotenv import load_dotenv
from ask_weather.utils.logger import get_logger
from ask_weather.utils.file_utils import load_prompt_template

import yaml
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

logger = get_logger(__file__)

class WeatherAgent:
    def __init__(self, env_path=".env", model="gpt-4o-mini", temperature=0, prompt_path="prompts/weather_agent_prompt.yaml"):
        if os.path.isfile(env_path):
            load_dotenv(dotenv_path=env_path)
            logger.info(f"successfully set env file")
        else:
            logger.error(f"환경 변수 파일을 찾을 수 없습니다: {env_path}")
            raise FileNotFoundError(f"{env_path} 파일이 존재하지 않습니다.")
    
        self.prompt_template = load_prompt_template(prompt_path)
        logger.info(f"프롬프트 템플릿 로드 완료: {prompt_path}")

        self.agent_executor = self.get_weather_agent(model, temperature)
        logger.info("initialized WeatherAgent")

    @tool
    @staticmethod
    def get_weather(location: str, date: str = None, hours: bool = False) -> str:
        """주어진 위치와 날짜에 대한 날씨 정보를 조회합니다."""
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        
        params = {
            "appid": api_key,
            "units": "metric"
        }
        
        # 위치의 위도와 경도 찾기
        # TODO 여러 개 목록에서 추출
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {
            "q": location,
            "limit": 1,
            "appid": api_key
        }
        
        try:
            geo_response = requests.get(geo_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
        except requests.exceptions.RequestException as e:
            logger.info("위치 정보를 가져오는데 실패했습니다.")
            return "위치 정보를 가져오는데 실패했습니다."
        
        if not geo_data:
            logger.info("위치를 찾을 수 없습니다.")
            return "위치를 찾을 수 없습니다."
        
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        params.update({"lat": lat, "lon": lon})

        # 날짜를 기준으로 API 호출 URL 설정
        base_url = ""
        if date:
            target_date = datetime.strptime(date, "%Y-%m-%d %H:%M" if hours else "%Y-%m-%d")
            current_date = datetime.now()
            logger.info(f"target_date: {target_date} current_date: {current_date}")

            # 과거 데이터
            if target_date < current_date:
                return "과거의 날씨는 현재 지원하지 않습니다."
                
            # 5일 예보 데이터
            elif target_date <= current_date + timedelta(days=5):
                base_url = "http://api.openweathermap.org/data/2.5/forecast"
                logger.info(f"5일 예보 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")
            
            # 16일 예보 데이터
            elif target_date <= current_date + timedelta(days=16):
                base_url = "https://pro.openweathermap.org/data/2.5/forecast/daily"
                params["cnt"] = (target_date - current_date).days + 1
                logger.info(f"16일 예보 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")

            # 30일 예보 데이터
            elif target_date <= current_date + timedelta(days=30):
                base_url = "https://pro.openweathermap.org/data/2.5/forecast/climate"
                logger.info(f"30일 예보 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")
        
        try:
            logger.debug(f"API 요청 - URL: {base_url}, 파라미터: {params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"API 요청 성공 - 상태 코드: {response.status_code}")

            if "list" in data:
                found_data = None
                minimum_timedelta = timedelta(days=32)
                for entry in data["list"]:
                    entry_date = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    if abs(entry_date - target_date) < minimum_timedelta:
                        found_data = entry
                        minimum_timedelta = abs(entry_date - target_date)
                
                if found_data:
                    weather_description = found_data["weather"][0]["description"]
                    temperature = found_data["main"]["temp"]
                    nearest_timedelta = found_data["dt_txt"]
                    return f"{location}의 {nearest_timedelta} 날씨: {weather_description}, 온도: {temperature}°C"
            else:
                return "해당 날씨 데이터를 찾을 수 없습니다."
    
        except requests.exceptions.RequestException as e:
            logger.info(f"날씨 정보를 가져오는데 실패했습니다: {e}")
            return f"날씨 정보를 가져오는데 실패했습니다. 오류: {str(e)}"

    def get_weather_agent(self, model="gpt-4o-mini", temperature=0, verbose=False, max_iterations=400, max_execution_time=60000, handle_parsing_errors=False):
        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = PromptTemplate.from_template(self.prompt_template)
        agent = create_react_agent(llm, [self.get_weather], prompt)
        return AgentExecutor(
            agent=agent, 
            tools=[self.get_weather], 
            verbose=verbose, 
            max_iterations=max_iterations,
            max_execution_time=max_execution_time,
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )
                
    def query(self, input_query, retry_count=1):
        for i in range(retry_count):
            try:
                response = self.agent_executor.invoke({"input": input_query})
                logger.info(f"response: {response}")
                return response["output"]
            except Exception as e:
                logger.error(f"Trial : {retry_count}, {e}")
        # TODO 실패 원인 케이스 정리
        return "날씨 정보를 가져오는데 실패했습니다."