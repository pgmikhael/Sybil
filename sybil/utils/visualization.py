import imageio
import numpy as np
import torch
import torch.nn.functional as F
from sybil.serie import Serie
from typing import Dict, List, Union
import os


def collate_attentions(
    attention_dict: Dict[str, np.ndarray], N: int, eps=1e-6
) -> np.ndarray:
    a1 = attention_dict["image_attention_1"]
    v1 = attention_dict["volume_attention_1"]

    a1 = torch.Tensor(a1)
    v1 = torch.Tensor(v1)

    # take mean attention over ensemble
    a1 = torch.exp(a1).mean(0)
    v1 = torch.exp(v1).mean(0)

    attention = a1 * v1.unsqueeze(-1)
    attention = attention.view(1, 25, 16, 16)

    attention_up = F.interpolate(
        attention.unsqueeze(0), (N, 512, 512), mode="trilinear"
    )
    attention_up = attention_up.cpu().numpy()
    attention_up = attention_up.squeeze()
    if eps:
        attention_up[attention_up <= eps] = 0.0

    return attention_up


def build_overlayed_images(
    images: List[np.ndarray], attention: np.ndarray, gain: int = 3
):
    overlayed_images = []
    N = len(images)
    for i in range(N):
        overlayed = np.zeros((512, 512, 3))
        overlayed[..., 2] = images[i]
        overlayed[..., 1] = images[i]
        overlayed[..., 0] = np.clip(
            (attention[i, ...] * gain * 256) + images[i],
            a_min=0,
            a_max=255,
        )

        overlayed_images.append(np.uint8(overlayed))

    return overlayed_images


def visualize_attentions(
    series: Union[Serie, List[Serie]],
    attentions: List[Dict[str, np.ndarray]],
    save_directory: str = None,
    gain: int = 3,
    attention_threshold: float = 1e-3,  # Ngưỡng attention tối thiểu
    # save_images_flag: bool = True  # Tùy chọn có lưu ảnh hay không
) -> List[List[np.ndarray]]:
    """
    Args:
        series (Serie): series object
        attentions (Dict[str, np.ndarray]): attention dictionary output from model
        save_directory (str, optional): where to save the images. Defaults to None.
        gain (int, optional): how much to scale attention values by for visualization. Defaults to 3.
        attention_threshold (float, optional): Minimum attention value to consider saving an image. Defaults to 1e-3.

    Returns:
        List[List[np.ndarray]]: list of list of overlayed images
    """
    print("=== visualize_attentions ===")
    if isinstance(series, Serie):
        series = [series]

    series_overlays = []
    for serie_idx, serie in enumerate(series):
        images = serie.get_raw_images()
        N = len(images)
        cur_attention = collate_attentions(attentions[serie_idx], N)

        overlayed_images = build_overlayed_images(images, cur_attention, gain)
        print("save_directory: ", save_directory)

        if save_directory is not None:
            save_path = os.path.join(save_directory, f"serie_{serie_idx}")

            # Lưu ảnh PNG chỉ khi attention vượt ngưỡng
            save_attention_images(
                overlayed_images,
                cur_attention,
                save_path,
                attention_threshold,
            )

            # Lưu toàn bộ ảnh dưới dạng GIF (nếu cần)
            save_images(overlayed_images, save_path, f"serie_{serie_idx}")

        series_overlays.append(overlayed_images)
    return series_overlays


def save_images(img_list: List[np.ndarray], directory: str, name: str):
    """
    Saves a list of images as a GIF in the specified directory with the given name.

    Args:
        ``img_list`` (List[np.ndarray]): A list of numpy arrays representing the images to be saved.
        ``directory`` (str): The directory where the GIF should be saved.
        ``name`` (str): The name of the GIF file.

    Returns:
        None
    """
    import imageio

    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{name}.gif")
    imageio.mimsave(path, img_list)
    print(f"GIF saved to: {directory}")


def save_attention_images(
    overlayed_images: List[np.ndarray],
    cur_attention: np.ndarray,
    save_path: str,
    attention_threshold: float,
):
    """
    Lưu các ảnh overlay có attention vượt ngưỡng.

    Args:
        overlayed_images (List[np.ndarray]): Danh sách ảnh đã overlay attention.
        cur_attention (np.ndarray): Attention values tương ứng với ảnh.
        save_path (str): Đường dẫn để lưu ảnh.
        attention_threshold (float): Ngưỡng attention để quyết định lưu ảnh.

    Returns:
        None
    """
    os.makedirs(save_path, exist_ok=True)
    for idx, (img, attention) in enumerate(zip(overlayed_images, cur_attention)):
        if np.max(attention) > attention_threshold:
            overlay_path = os.path.join(save_path, f"slice_{idx}.png")
            print(f"Saving overlay image to: {overlay_path}")  # Debug
            imageio.imwrite(overlay_path, img)  # Lưu ảnh PNG
