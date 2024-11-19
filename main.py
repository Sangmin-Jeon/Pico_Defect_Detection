from Network.ApiService import ApiService


if __name__ == "__main__":
    apiManager = ApiService()
    _ = apiManager.post_submit(name="stu", student_number="stu_num")