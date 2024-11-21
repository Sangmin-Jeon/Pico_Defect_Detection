import os
from torchvision import transforms
from PIL import Image


def augment_images(directory_path, save_directory=None, augmentations=None):
    # 기본 데이터 증강 설정
    if augmentations is None:
        '''
        데이터 증강 기법은 다양합니다.
        transforms. 으로 어떤 방식으로 데이터 증강을 할것인가를 정하게 되는데
        원하는 기법을 설정하면 됩니다.
        '''
        augmentations = transforms.Compose([
            # 이미지를 수평 방향으로 뒤집습니다. 뒤집힐 확률은 50%입니다.
            transforms.RandomHorizontalFlip(p=0.5),
            # 이미지를 수직 방향으로 뒤집습니다. 뒤집힐 확률은 50%입니다.
            transforms.RandomVerticalFlip(p=0.5),
            # 이미지의 색상을 무작위로 변경합니다.
            # - brightness: 밝기를 ±50% 범위에서 조정합니다.
            # - contrast: 대비를 ±50% 범위에서 조정합니다.
            # - saturation: 채도를 ±50% 범위에서 조정합니다.
            # - hue: 색조를 ±10% 범위에서 조정합니다.
            transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.1),
            # 이미지를 -30도에서 +30도 사이에서 무작위로 회전합니다.
            transforms.RandomRotation(degrees=30),
            # 이 값은 현재 사용하는 이미지의 표준 크기와 일치하며, 변경할 수 있습니다.
            # 원래 사용하던 크기가 640, 480 사이즈에요.
            transforms.Resize((640, 480))
        ])

    image_files = [file for file in os.listdir(directory_path) if file.lower().endswith(('.jpg'))]
    augmented_images = []

    for img_file in image_files:
        image_path = os.path.join(directory_path, img_file)
        image = Image.open(image_path).convert("RGB")

        augmented_image = augmentations(image)
        augmented_images.append(augmented_image)

        if save_directory:
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory, f"aug_{img_file}")
            augmented_image.save(save_path)

    return augmented_images


def set_data_augment(directory_path, store_directory_path):
    # 여기서 입력 및 출력 디렉토리를 설정 하면 됩니다.
    input_dir = directory_path # 여기에 데이터 증강 시킬 이미지의 경로 넣으세요.
    output_dir = store_directory_path # 저장할 경로 넣으세요.

    augmented_images = augment_images(input_dir, save_directory=output_dir)
    print(f"={len(augmented_images)}개의 이미지들 데이터 증강 완료")