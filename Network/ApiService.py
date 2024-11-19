from Network.NetworkManager import NetworkManager
from Models.StudentModel import Student


class ApiService:
    def __init__(self):
        self.networkManager = NetworkManager()

    def post_submit(self, name, student_number):
        params = Student(name=name, student_number=student_number)
        return self.networkManager.post("submit", json=params.__dict__)

    """새로운 API 사용시 추가"""

