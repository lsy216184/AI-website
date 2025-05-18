from PIL import Image
import torch
import timm
import yaml
from timm.data import resolve_model_data_config, create_transform

# 초기화는 1번만 실행
model_name = "vit_mediumd_patch16_reg4_gap_256.sbb_in12k_ft_in1k"
model = timm.create_model(model_name, pretrained=True).eval()

yaml_path = "/root/test/timm/imagenet.yaml"
with open(yaml_path, "r") as f:
    data = yaml.safe_load(f)
imagenet_classes = [data["names"][i] for i in sorted(data["names"].keys())]

def classify_image(img_path):
    img = Image.open(img_path).convert("RGB")
    config = resolve_model_data_config(model)
    transform = create_transform(**config, is_training=False)
    input_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        top5_prob, top5_idx = torch.topk(output.softmax(dim=1) * 100, k=1)

    predictions = [
        {
            "class_name": imagenet_classes[idx.item()],
            "probability": prob.item()
        }
        for idx, prob in zip(top5_idx[0], top5_prob[0])
    ]
    return predictions
