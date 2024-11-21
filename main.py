from Network.ApiService import ApiService
from Tools.DataAugment import set_data_augment
from Tools.Gradio import start_gradio
from Tools.CheckImage import show_imaged

# 여기에 모델 API URL 을 넣으면 됩니다.
VISION_API_URL = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/9a987f3f-174c-4678-acb2-60be9ea6a0ee/inference"
TEAM = "kdt2024_1-9" # 이건 건들 필요 없어요.
ACCESS_KEY = "Superb AI 사이트에 로그인 해서 넣으세요." # 이건 본인 setting -> ACCESS KEY를 직접 넣어서 사용하세요.
directory_path = "본인 컴퓨터에 이미지를 저장한 디렉토리 경로 넣으세요."

'''
    여기에 필요한 기능을 주석 해제 하여 사용하세요 !!!
'''

''' 1. 데이터 증강 시 사용 (학습 데이터 만들때) '''
# 1번 param에 데이터 증강 시킬 이미지의 경로 넣으세요.
# 2번 param에 저장할 경로 넣으세요.
set_data_augment("", "")

''' 2. gradio 웹 사용 (이미지 직접 업로드)'''
# start_gradio(VISION_API_URL, TEAM, ACCESS_KEY)

''' 3. 추론 한 이미지 확인 '''
# 1번에 directory_path에 추론할 이미지의 경로 넣으세요.
# show_imaged("", VISION_API_URL, ACCESS_KEY)


if __name__ == "__main__":
    # apiManager = ApiService()
    # _ = apiManager.post_submit(name="stu", student_number="stu_num")
    pass


