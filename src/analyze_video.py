import cv2
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torchreid
from torchvision import transforms
from ultralytics import YOLO
import os

from config.constants import MESSAGES

def analyze_video(file_name, save_dir):
    video_path = os.path.join(save_dir, f"{file_name}.mp4")

    if not os.path.exists(video_path):
        raise FileNotFoundError(MESSAGES.ERROR.NOT_FOUND_VIDEO)

    model = YOLO("yolo11n.pt")

    reid_model = torchreid.models.build_model(name='resnet50', num_classes=751, pretrained=True)

    reid_model.eval()

    if torch.cuda.is_available():
        reid_model = reid_model.cuda()

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((256, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    results = model.track(
        project=save_dir,
        name="result",
        source=video_path,
        tracker="botsort.yaml",
        save=True,
        imgsz=320,
        vid_stride=2,
        stream=True
    )

    id_mapping = {}
    prev_features = {}

    try:
        for frame_idx, result in enumerate(results):
            if result.boxes.id is not None:
                ids = result.boxes.id.cpu().numpy()
                boxes = result.boxes.xyxy.cpu().numpy()

                for i, (obj_id, box) in enumerate(zip(ids, boxes)):
                    img = result.orig_img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

                    if img.size == 0:
                        continue

                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img_tensor = transform(img).unsqueeze(0)

                    if torch.cuda.is_available():
                        img_tensor = img_tensor.cuda()

                    with torch.no_grad():
                        features = reid_model(img_tensor).cpu().numpy()

                    if prev_features:
                        max_sim = 0
                        matched_id = None

                        for prev_id, prev_feat in prev_features.items():
                            sim = cosine_similarity(features, prev_feat)[0][0]

                            if sim > max_sim and sim > 0.7:
                                max_sim = sim
                                matched_id = prev_id

                        if matched_id is not None:
                            id_mapping[obj_id] = matched_id
                        else:
                            id_mapping[obj_id] = obj_id
                    else:
                        id_mapping[obj_id] = obj_id
                    prev_features[obj_id] = features
    except:
        raise RuntimeError(MESSAGES.ERROR.FAILED_ANALYZE)