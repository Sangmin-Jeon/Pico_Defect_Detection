import requests
from threading import Lock
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkManager:
    _instance = None  # 클래스의 단일 인스턴스를 저장
    _lock = Lock()  # 멀티스레드 환경에서 안전하게 인스턴스를 생성하기 위한 락

    def __new__(cls):
        with cls._lock:  # 락을 걸어 스레드 안전성을 보장
            if cls._instance is None:
                cls._instance = super(NetworkManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # 인스턴스가 이미 초기화되었는지 확인
            self._initialized = True
            # self.base_url = "https://requests-homework.onrender.com"
            self.base_url = "http://192.168.10.14:8888"
            self.headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
            }
            logging.basicConfig(level=logging.INFO)

    # GET 메서드
    def get(self, endpoint, params=None, json=None, is_team=False):
        return self.__request("GET", endpoint, params=params, json=json, is_team=is_team)

    # POST 메서드
    def post(self, endpoint, params=None, json=None, files=None, is_team=False):
        return self.__request("POST", endpoint, params=params, json=json, files=files, is_team=is_team)

    """새로운 HTTP 메서드 사용시 추가"""

    def __request(self, method, endpoint, is_team, params=None, files=None, json=None):
        # Base URL 설정
        if is_team:
            url = f"http://192.168.10.14:8884/{endpoint}"
        else:
            url = f"{self.base_url}/{endpoint}"

        # 로깅 추가
        logger.info(f"Sending {method} request to {url} with params={params}, json={json}, files={files}")

        try:
            # 요청 전송
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=json,
                files=files,
                headers=self.headers,
            )

            # 응답 상태 확인
            response.raise_for_status()
            logger.info(f"Response status code: {response.status_code}")

            if 200 <= response.status_code < 300:
                logger.info(f"Received response: {response.status_code} {response.text}")
                return response.json()
            else:
                # 상태 코드가 3xx, 4xx, 5xx인 경우에 대한 추가 로깅
                if 300 <= response.status_code < 400:
                    logger.warning(f"Redirection: {response.status_code} {response.text}")
                elif 400 <= response.status_code < 500:
                    logger.error(f"Client error: {response.status_code} {response.text}")
                elif 500 <= response.status_code < 600:
                    logger.error(f"Server error: {response.status_code} {response.text}")
                return {"error": f"Unexpected response: {response.status_code} {response.text}"}

        # 요청 타임아웃 처리
        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            return {"error": "The request timed out."}

        # 리디렉션이 너무 많을 때 처리
        except requests.exceptions.TooManyRedirects:
            logger.error("Too many redirects")
            return {"error": "Too many redirects."}

        # 네트워크 연결 오류 처리
        except requests.exceptions.ConnectionError:
            logger.error("Network connection error")
            return {"error": "Network connection error."}

        # 그 외 모든 예외 처리
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}