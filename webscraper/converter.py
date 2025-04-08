import torch, cv2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.model_zoo import model_zoo

# Modeli ayarla
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

predictor = DefaultPredictor(cfg)

# Görseli oku
image = cv2.imread("ayakkabili_gorsel.jpg")
outputs = predictor(image)

# Maske çıkar
masks = outputs["instances"].pred_masks.to("cpu").numpy()

# Sadece ayakkabı sınıfını filtrele
shoe_class_ids = [47]  # COCO datasetindeki "shoe" ID'si
filtered_masks = np.any(masks[outputs["instances"].pred_classes.numpy() == shoe_class_ids], axis=0)

# Ayakkabıyı çıkar
image[filtered_masks] = [255, 255, 255]  # Beyaz arka plan yap
cv2.imwrite("ayakkabisiz_gorsel.jpg", image)
