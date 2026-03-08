import os


class Config:
    """全局配置类，集中管理项目所有配置参数。"""

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    OCR_USE_GPU = False
    OCR_LANG = "ch"
    OCR_DET_MODEL_DIR = None
    OCR_REC_MODEL_DIR = None
    OCR_CLS_MODEL_DIR = None
    OCR_SHOW_LOG = False

    SEAL_HSV_LOWER1 = (0, 40, 40)
    SEAL_HSV_UPPER1 = (15, 255, 255)
    SEAL_HSV_LOWER2 = (165, 40, 40)
    SEAL_HSV_UPPER2 = (180, 255, 255)
    SEAL_BLACK_THRESHOLD = 80
    SEAL_KERNEL_SIZE = (5, 5)
    SEAL_MIN_AREA = 100
    SEAL_MIN_CROP_SIZE = 200
    SEAL_MAX_CROP_SIZE = 500

    LOG_LEVEL = "INFO"
