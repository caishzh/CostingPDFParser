import os

class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    OCR_USE_GPU = False
    OCR_LANG = "ch"
    OCR_DET_MODEL_DIR = None
    OCR_REC_MODEL_DIR = None
    OCR_CLS_MODEL_DIR = None
    OCR_SHOW_LOG = False
    
    SEAL_HSV_LOWER1 = (0, 70, 70)
    SEAL_HSV_UPPER1 = (10, 255, 255)
    SEAL_HSV_LOWER2 = (170, 70, 70)
    SEAL_HSV_UPPER2 = (180, 255, 255)
    SEAL_BLACK_THRESHOLD = 50
    SEAL_KERNEL_SIZE = (3, 3)
    SEAL_MIN_AREA = 200
    SEAL_MIN_CROP_SIZE = 300
    SEAL_MAX_CROP_SIZE = 400
    
    LOG_LEVEL = "INFO"
