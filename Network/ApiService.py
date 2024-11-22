from Network.NetworkManager import NetworkManager
from Models.StudentModel import Student


class ApiService:
    def __init__(self):
        self.networkManager = NetworkManager()

    def post_submit(self, name, student_number):
        params = Student(name=name, student_number=student_number)
        return self.networkManager.post("submit", json=params.__dict__)

    """새로운 API 사용시 추가"""

    # 192.169.10.13 서버 open
    def post_start_server(self, team, model_id):
        return self.networkManager.post("start-server", json=(team, model_id))

