# ocr_stable.py - PaddleOCR 稳定封装（自动 GPU/CPU 降级）
"""
PaddleOCR 稳定调用接口
- 自动检测 GPU 可用性，失败则降级到 CPU
- 启动时自检模型文件
- 提供健康检查函数
"""
import os
import sys
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# PaddleOCR 模型路径（优先使用工作目录备份）
WORKSPACE_MODELS = r'C:\Users\Administrator\.openclaw\workspace\models\paddleocr'
PADDLE_CACHE = os.path.expanduser(r'C:\Users\Administrator\.paddleocr')

# 全局 OCR 引擎实例
_ocr_engine = None
_ocr_mode = None  # 'gpu' 或 'cpu'


def _check_gpu_available():
    """检测 GPU 是否可用"""
    try:
        import paddle
        paddle.device.set_device('gpu:0')
        x = paddle.to_tensor([1.0])
        del x
        return True
    except Exception as e:
        logger.warning(f"GPU 检测失败: {e}")
        return False


def _check_models_exist():
    """检查模型文件是否存在"""
    required_dirs = ['det', 'rec', 'cls']
    for d in required_dirs:
        path = os.path.join(PADDLE_CACHE, 'whl', d)
        if not os.path.exists(path):
            logger.warning(f"模型目录缺失: {path}")
            return False
    return True


def _init_ocr_gpu():
    """初始化 GPU 模式"""
    try:
        from paddleocr import PaddleOCR
        logger.info("尝试初始化 PaddleOCR GPU 模式...")
        ocr = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            use_gpu=True,
            show_log=False
        )
        logger.info("PaddleOCR GPU 模式初始化成功")
        return ocr, 'gpu'
    except Exception as e:
        logger.warning(f"GPU 模式初始化失败: {e}")
        return None, None


def _init_ocr_cpu():
    """初始化 CPU 模式"""
    try:
        from paddleocr import PaddleOCR
        logger.info("尝试初始化 PaddleOCR CPU 模式...")
        ocr = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            use_gpu=False,
            show_log=False
        )
        logger.info("PaddleOCR CPU 模式初始化成功")
        return ocr, 'cpu'
    except Exception as e:
        logger.error(f"CPU 模式初始化也失败: {e}")
        return None, None


def init():
    """
    初始化 PaddleOCR 引擎
    优先 GPU，失败自动降级 CPU
    返回: (引擎实例, 模式字符串)
    """
    global _ocr_engine, _ocr_mode

    if _ocr_engine is not None:
        return _ocr_engine, _ocr_mode

    # Step 1: 检查模型文件
    if not _check_models_exist():
        logger.error("模型文件缺失，无法初始化")
        return None, None

    # Step 2: 尝试 GPU 模式
    ocr, mode = _init_ocr_gpu()
    if ocr is not None:
        _ocr_engine = ocr
        _ocr_mode = mode
        # 预热（用已有的测试图片）
        warmup_img = r'C:\Users\Administrator\Desktop\ocr_test.png'
        if os.path.exists(warmup_img):
            try:
                _ = _ocr_engine.ocr(warmup_img, cls=True)
                logger.info(f"预热完成 (GPU)")
            except Exception as w:
                logger.warning(f"预热失败: {w}")
        return ocr, mode

    # Step 3: GPU 失败，降级 CPU
    ocr, mode = _init_ocr_cpu()
    if ocr is not None:
        _ocr_engine = ocr
        _ocr_mode = mode
        # 预热
        warmup_img = r'C:\Users\Administrator\Desktop\ocr_test.png'
        if os.path.exists(warmup_img):
            try:
                _ = _ocr_engine.ocr(warmup_img, cls=True)
                logger.info(f"预热完成 (CPU)")
            except Exception as w:
                logger.warning(f"预热失败: {w}")
        return ocr, mode

    logger.error("PaddleOCR 所有模式均初始化失败")
    return None, None


def ocr_image(image_path, return_coords=False):
    """
    对图片进行 OCR 识别

    参数:
        image_path: 图片路径
        return_coords: 是否返回坐标信息

    返回:
        如果 return_coords=False: [(文本, 置信度), ...]
        如果 return_coords=True:  [(文本, 置信度, (x1,y1,x2,y2)), ...]
    """
    global _ocr_engine, _ocr_mode

    # 延迟初始化
    if _ocr_engine is None:
        engine, mode = init()
        if engine is None:
            raise RuntimeError("PaddleOCR 初始化失败")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    result = _ocr_engine.ocr(image_path, cls=True)

    if not result or not result[0]:
        return []

    outputs = []
    for line in result[0]:
        box = line[0]
        text = line[1][0]
        confidence = line[1][1]
        if return_coords:
            outputs.append((text, confidence, box))
        else:
            outputs.append((text, confidence))

    return outputs


def health_check():
    """
    健康检查 - 验证 PaddleOCR 是否可用

    返回:
        dict: {
            'status': 'ok' / 'degraded' / 'error',
            'mode': 'gpu' / 'cpu' / None,
            'message': str,
            'time_ms': float  # 初始化耗时
        }
    """
    start = time.time()

    # 检查模型
    if not _check_models_exist():
        return {
            'status': 'error',
            'mode': None,
            'message': '模型文件缺失',
            'time_ms': (time.time() - start) * 1000
        }

    # 检查 GPU
    gpu_ok = _check_gpu_available()

    # 尝试初始化/使用引擎
    global _ocr_engine
    if _ocr_engine is None:
        ocr, mode = init()
        if ocr is None:
            return {
                'status': 'error',
                'mode': None,
                'message': '引擎初始化失败',
                'time_ms': (time.time() - start) * 1000
            }
    else:
        mode = _ocr_mode

    # 执行一个简单的 OCR 测试
    try:
        test_img = r'C:\Users\Administrator\Desktop\ocr_test.png'
        if os.path.exists(test_img):
            result = _ocr_engine.ocr(test_img, cls=True)
            if result and result[0]:
                status = 'ok' if mode == 'gpu' else 'degraded'
                return {
                    'status': status,
                    'mode': mode,
                    'message': f'正常 ({mode}模式)',
                    'time_ms': (time.time() - start) * 1000
                }
            else:
                return {
                    'status': 'degraded',
                    'mode': mode,
                    'message': 'OCR 无输出',
                    'time_ms': (time.time() - start) * 1000
                }
        else:
            # 没有测试图片，只检查初始化状态
            status = 'ok' if mode == 'gpu' else 'degraded'
            return {
                'status': status,
                'mode': mode,
                'message': f'已初始化 ({mode}模式)',
                'time_ms': (time.time() - start) * 1000
            }
    except Exception as e:
        pass

    return {
        'status': 'degraded',
        'mode': mode,
        'message': 'OCR 可用但测试异常',
        'time_ms': (time.time() - start) * 1000
    }


def reset():
    """重置引擎实例（用于重新初始化）"""
    global _ocr_engine, _ocr_mode
    _ocr_engine = None
    _ocr_mode = None
    logger.info("OCR 引擎已重置")


if __name__ == '__main__':
    # 独立测试
    print("=" * 50)
    print("PaddleOCR 健康检查")
    print("=" * 50)

    result = health_check()
    print(f"状态: {result['status']}")
    print(f"模式: {result['mode']}")
    print(f"消息: {result['message']}")
    print(f"耗时: {result['time_ms']:.1f}ms")
