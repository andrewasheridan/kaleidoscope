import sys
import cv2
import numpy as np

from itertools import takewhile

# for type hinting / annotations
from typing import List, Dict, Any, Union, Tuple


def generate_basic_metadata(filenames: List[str]) -> Dict[str, Any]:
    """

    :param filenames: 
    :rtype: Dict[str, Any] 
    """
    num_files: int = len(filenames)
    image_metadata: Dict[str, Any] = {}

    i: int
    filename: str
    for i, filename in enumerate(filenames):
        image: Union[np.ndarray, None] = cv2.imread(filename)

        height: int
        width: int
        channels: int
        height, width, channels = image.shape

        std: float
        mean: float
        minimum: float
        maximum: float
        pixel_sum: float
        std, mean, minimum, maximum, pixel_sum = (
            image.std(),
            image.mean(),
            image.min(),
            image.max(),
            image.sum(),
        )

        image_metadata[filename] = {
            "height": height,
            "width": width,
            "area": height * width,
            "channels": channels,
            "std": std,
            "mean": mean,
            "min": minimum,
            "max": maximum,
            "sum": pixel_sum,
        }

        sys.stdout.write("\r{:.2f}%".format(100 * (i + 1) / num_files))
    sys.stdout.write("\n")
    return image_metadata


def determine_mean_image_area(metadata: Dict[str, Any]) -> float:

    areas: List[float] = []

    image_metadata: Dict[str, Any]
    for image_metadata in metadata.values():

        area: float
        area = image_metadata["height"] * image_metadata["width"]
        areas.append(area)

    mean_area: float = np.mean(areas)
    return mean_area


def get_image_name_from_path(path: str) -> str:

    s: str = path[::-1]
    s = "".join(takewhile(lambda x: x != "/", s))[::-1]
    return s


def normalize_image_areas(filenames: List[str], metadata: Dict[str, Any]) -> None:
    """
    :param metadata:
    :param filenames:
    :rtype: None
    """
    num_files: int = len(filenames)

    mean_area: float = determine_mean_image_area(metadata)
    new_side_len: int = int(np.sqrt(mean_area))

    i: int
    filename: str
    for i, filename in enumerate(filenames):

        image: Union[np.ndarray, None] = cv2.imread(filename)

        height: int
        width: int
        height, width, _ = image.shape

        if height < width:
            new_height: int = new_side_len
            new_width: int = int(width * new_height / height)

            new_size: Tuple[int, int] = (new_width, new_height)

        else:
            new_width: int = new_side_len
            new_height:int = int(height * new_width / width)

            new_size = (new_width, new_height)

        image: np.ndarray = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)
        image_name: str = get_image_name_from_path(filename)
        cv2.imwrite("area_normalized/" + image_name, image)

        sys.stdout.write("\r{:.2f}%".format(100 * (i + 1) / num_files))

    return None
