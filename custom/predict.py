#!/usr/bin/env python

__doc__ = """
Use Sybil to run inference on a single exam.
"""
import os
import sys

__dir__ = os.path.dirname(__file__)
print(os.path.join(__dir__, "../"))
sys.path.append(os.path.join(__dir__, "../"))

import json
import os
import pickle
import typing
from typing import Literal


from sybil.utils import logging_utils
from sybil.datasets import utils
from sybil import Serie, Sybil, __version__
# CODE ĐỂ BIẾT CHƯƠNG TRINH CHAY TỪ a-b, CÁC THAM SỐ GỐC
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from scipy.ndimage import zoom
import pydicom

from visualization import visualize_attentions


def predict(
    image_dir,
    output_dir,
    model_name="sybil_ensemble",
    return_attentions=False,
    write_attention_images=False,
    file_type: Literal["auto", "dicom", "png"] = "auto",
    threads: int = 0,
):
    print("=== predict start ===")
    logger = logging_utils.get_logger()

    return_attentions |= write_attention_images

    input_files = os.listdir(image_dir)
    input_files = [
        os.path.join(image_dir, x) for x in input_files if not x.startswith(".")
    ]
    input_files = [x for x in input_files if os.path.isfile(x)]

    voxel_spacing = None
    if file_type == "auto":
        extensions = {os.path.splitext(x)[1] for x in input_files}
        extension = extensions.pop()
        if len(extensions) > 1:
            raise ValueError(
                f"Multiple file types found in {image_dir}: {','.join(extensions)}"
            )

        file_type = "dicom"
        if extension.lower() in {".png", "png"}:
            file_type = "png"
            voxel_spacing = utils.VOXEL_SPACING
            logger.debug(f"Using default voxel spacing: {voxel_spacing}")
    assert file_type in {"dicom", "png"}
    file_type = typing.cast(Literal["dicom", "png"], file_type)

    num_files = len(input_files)

    logger.debug(
        f"Beginning prediction using {num_files} {file_type} files from {image_dir}"
    )

    print(f"Beginning prediction using {num_files} {file_type} files from {image_dir}")

    # Load a trained model
    model = Sybil(model_name)

    # Get risk scores
    serie = Serie(input_files, voxel_spacing=voxel_spacing, file_type=file_type)
    series = [serie]
    prediction = model.predict(
        series, return_attentions=return_attentions, threads=threads
    )
    # Extract attentions
    # attentions = prediction.attentions
    prediction_scores = prediction.scores[0]

    logger.debug(f"Prediction finished. Results:\n{prediction_scores}")
    print("prediction_scores", prediction_scores)
    prediction_path = os.path.join(output_dir, "prediction_scores.json")
    pred_dict = {"predictions": prediction.scores}
    with open(prediction_path, "w") as f:
        json.dump(pred_dict, f, indent=2)

    series_with_attention = None
    if return_attentions:
        print("return_attentions")
        attention_path = os.path.join(output_dir, "attention_scores.pkl")
        with open(attention_path, "wb") as f:
            pickle.dump(prediction, f)

    if write_attention_images:
        print("write_attention_images")
        series_with_attention = visualize_attentions(
            series,
            attentions=prediction.attentions,
            save_directory=output_dir,
            gain=3,
        )

    return pred_dict, series_with_attention


def main():
    print("=== main ===")
    # 1-2da413541bb2518fb0f8c583900999ef.dcm
    image_dir = "D:/Work/Clients/Job/Sybil/custom/Chung_20241014"
    output_dir = "./visualizations"
    model_name = "sybil_ensemble"
    return_attentions = True
    write_attention_images = True

    os.makedirs(output_dir, exist_ok=True)
    print("predict")
    pred_dict, series_with_attention = predict(
        image_dir,
        output_dir,
        model_name,
        return_attentions,
        write_attention_images,
    )
    print(json.dumps(pred_dict, indent=2))


if __name__ == "__main__":
    main()
