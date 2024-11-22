from Network.ApiService import ApiService
# from Tools.DataAugment import set_data_augment
# from Tools.Gradio import start_gradio
# from Tools.CheckImage import show_imaged
import time
import Inference_Pico
import requests
import os
import time

# 여기에 모델 API URL 을 넣으면 됩니다.
VISION_API_URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/9a987f3f-174c-4678-acb2-60be9ea6a0ee/inference"
TEAM = "kdt2024_1-9" # 이건 건들 필요 없어요.
ACCESS_KEY = "fFJOF6bXM75WTU3qTKADi2DfJRVpcJXk5vAdEep2" # 이건 본인 setting -> ACCESS KEY를 직접 넣어서 사용하세요.
directory_path = "/Users/jeonsangmin/Desktop/broken_img_"
store_directory_path = "/Users/jeonsangmin/Desktop/v2/증강데이터"

'''
    여기에 필요한 기능을 주석 해제 하여 사용하세요 !!!
'''

''' 1. 데이터 증강 시 사용 (학습 데이터 만들때) '''
# 1번 param에 데이터 증강 시킬 이미지의 경로 넣으세요.
# 2번 param에 저장할 경로 넣으세요.
# set_data_augment(directory_path, store_directory_path)

''' 2. gradio 웹 사용 (이미지 직접 업로드)'''
# start_gradio(VISION_API_URL, TEAM, ACCESS_KEY)

''' 3. 추론 한 이미지 확인 (아직 작업 중)'''
# 1번에 directory_path에 추론할 이미지의 경로 넣으세요.
# show_imaged("", VISION_API_URL, ACCESS_KEY)


# if __name__ == "__main__":
#     apiManager = ApiService()
#     # _ = apiManager.post_submit(name="stu", student_number="stu_num")
#     _ = apiManager.post_start_server(team='team4', model_id='2cbabb7e-5f5c-47c3-ab03-3b7c9ad3fa5e')
#     time.sleep(1)
#     img_inf = apiManager.post_inference(0.3, "YOLOv6-M", '/home/rokey/Downloads/b4_img_266.jpg')
#     Inference_Pico.show_imaged('/home/rokey/Downloads/b4_img_266.jpg', img_inf)



def test_image_detection():
    # API endpoint URL
    url = "http://192.168.10.14:8884/inference/run"  # Adjust port if different

    # Test image path - adjust this to your image location
    image_path = "/home/rokey/Downloads/b4_img_266.jpg"

    # Parameters
    params = {
        "min_confidence": 0.31,
        "base_model": "YOLOv6-M"  # YOLOv6-N, YOLOv6-M, YOLOv6-L, YOLOv6-L6
    }

    # Prepare the file
    with open(image_path, 'rb') as image_file:
        files = {'file': ('image.jpg', image_file, 'image/jpeg')}

        # Send POST request
        response = requests.post(url, params=params, files=files)

    # Check if request was successful
    if response.status_code == 200:
        print("Success!")
        print("Detected objects:", response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def test_start_server():
    # API endpoint URL
    url = "http://192.168.10.14:8888/start-server/team4"  # Adjust host/port and team name
    # Parameters
    params = {
        "model_id": "2cbabb7e-5f5c-47c3-ab03-3b7c9ad3fa5e"  # Replace with actual model ID
    }

    # Send POST request
    response = requests.post(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        print("Server started successfully!")
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    # Test both endpoints
    print("Testing server start...")
    # test_start_server()

    # time.sleep(1)

    print("\nTesting image detection...")
    data = test_image_detection()
    Inference_Pico.show_imaged("/home/rokey/Downloads/b4_img_266.jpg", data)