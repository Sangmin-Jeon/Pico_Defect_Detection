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
        params = { "model_id": model_id }
        return self.networkManager.post("start-server/" + team, params=params, is_team=False)

    def post_inference(self, min_confidence, base_model, file_path):
        params = {
            "min_confidence": min_confidence,
            "base_model": base_model
        }
        with open(file_path, 'rb') as image_file:
            files = {'file': ('b4_img_266.jpg', image_file, 'image/jpeg')}
            return self.networkManager.post("inference/run", params=params, files=files, is_team=True)
