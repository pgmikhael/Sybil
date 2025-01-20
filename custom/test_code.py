import os

import numpy as np
from sybil import Sybil, Serie
from sybil import visualize_attentions
name_or_path = []

# Load the pretrained model
model = Sybil("sybil_ensemble")
print("Model loaded successfully", model)
# Load the DICOM file
dicom_path_1 = "D:/Work/Clients/Job/Sybil/custom/1-2da413541bb2518fb0f8c583900999ef.dcm"
serie = Serie([dicom_path_1])

# Get risk scores and attention results
prediction = model.predict([serie], return_attentions=True)
# print("scores:", prediction)

# # Extract attentions
# attentions = prediction.attentions

# # Ensure the save directory exists
# save_directory = "./visualizations"
# os.makedirs(save_directory, exist_ok=True)

# # # You can also evaluate by providing labels
# # serie = Serie([dicom_path_1], label=1)
# # results = model.evaluate([serie])
# print("Attention size:", len(attentions))

# # # Normalize image attention for debugging or visualization
# # normalized_attention = (
# #     attentions[0]['image_attention_1'] - np.min(attentions[0]['image_attention_1'])
# # ) / (np.max(attentions[0]['image_attention_1']) - np.min(attentions[0]['image_attention_1']))

# # # Thay thế image_attention_1 bằng normalized_attention trong attentions
# # attentions[0]['image_attention_1'] = normalized_attention

# # # Đảm bảo các phần còn lại trong cấu trúc attentions vẫn giữ nguyên
# # print("Updated attentions structure:")
# # print(attentions[0].keys())  # Xác nhận các khóa còn lại không bị thay đổi

# # # Debugging: Print the normalized attention map
# # print("Normalized attention (first slice):", normalized_attention[0][0][:10])

# # print("Image attention (first slice):", attentions[0]['image_attention_1'][0][0][:10])
# # print("Volume attention:", attentions[0]['volume_attention_1'][0])

# # Visualize attentions
# series_with_attention = visualize_attentions(
#     [serie],  # Ensure this is a list of Series
#     attentions=attentions,
#     save_directory=save_directory,
#     gain=10,
# )


# print(f"Attention visualizations saved to {save_directory}")