import yaml
from ask_weather.utils.logger import get_logger

logger = get_logger(__file__)

def load_prompt_template(prompt_path):
    """YAML 파일에서 프롬프트 템플릿을 로드합니다."""
    try:
        with open(prompt_path, 'r') as file:
            prompt_data = yaml.safe_load(file)
            return prompt_data['template']
    except Exception as e:
        logger.error(f"프롬프트 템플릿을 로드하는데 실패했습니다: {e}")
