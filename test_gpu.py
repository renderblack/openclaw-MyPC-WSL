import paddle
print('PaddlePaddle version:', paddle.__version__)
try:
    print('GPU count:', paddle.device.cuda.device_count())
except Exception as e:
    print('GPU check error:', e)