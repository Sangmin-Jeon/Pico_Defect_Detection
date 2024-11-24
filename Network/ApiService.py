from Network.NetworkManager import NetworkManager
from Models.StudentModel import Student


class ApiService:
    def __init__(self):
        self.networkManager = NetworkManager()

    def post_submit(self, name, student_number):
        params = Student(name=name, student_number=student_number)
        return self.networkManager.post("submit", json=params.__dict__)

    """새로운 API 사용시 추가"""

    # 192.169.10.14 서버 open
    def post_start_server(self, team, model_id):
        params = {"model_id": model_id}
        try:
            return self.networkManager.post(f"start-server/{team}", params=params, is_team=False)
        except Exception as e:
            print(f"Error in post_start_server: {e}")
            raise

    def post_inference(self, min_confidence, base_model, file_path):
        if not file_path:
            raise ValueError("File path is required for inference.")

        params = {
            "min_confidence": min_confidence,
            "base_model": base_model
        }

        try:
            with open(file_path, 'rb') as image_file:
                files = {'file': ('image.jpg', image_file, 'image/jpeg')}
                return self.networkManager.post("inference/run", params=params, files=files, is_team=True)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            raise
        except Exception as e:
            print(f"Error in post_inference: {e}")
            raise