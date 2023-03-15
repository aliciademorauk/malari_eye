import torch

# fetching model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Image
img = 'malaria_data/images/0a7bfa8a-ee52-4f7a-b9c5-2919ecfa93ef.png'
# Inference
results = model(img)
# Results, change the flowing to: results.show()
# results.show()  # or .show(), .save(), .crop(), .pandas(), etc
# results.xyxy[0]  # im predictions (tensor)
result_df = results.pandas().xyxy[0]  # im predictions (pandas)
result_df
