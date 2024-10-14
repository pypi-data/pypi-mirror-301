"""
ntanh

An python parametters library.
"""

__version__ = "0.1.6"
__author__ = "Nguyễn Tuấn Anh - nt.anh.fai@gmail.com"
__credits__ = "MIT License"

from ntanh.yolo_boxes import xyxy_to_yolo_str, yolo_str_to_xyxy
from . import ParamsBase

__help__ = """
from ntanh.ParamsBase import tactParametters
from ntanh.yolo_boxes import xyxy_to_yolo_str, yolo_str_to_xyxy
"""


def info():
    print(
        """
          # Giới thiệu

ntanh là một thư viện các nhiệm vụ hàng ngày sử dụng, hay dùng nhưng không khó, mất thời gian code cho các dự án lẻ tẻ.

# Cài đặt
`pip install ntanh`

# Cách dùng:

```python
from pprint import pprint
from ntanh.ParamsBase import tactParametters
import ntanh

print(ntanh.__version__)
mParams = tactParametters()

fns = mParams.fnFIS(r"../", exts=(".py"))
pprint(fns)
```

Kết quả:

```
'0.1.4'
['../tact/setup.py',
 '../tact/__init__.py',
 '../tact/build/lib/ntanh/ParamsBase.py',
 '../tact/build/lib/ntanh/__init__.py',
 '../tact/build/lib/tact/ParamsBase.py',
 '../tact/build/lib/tact/__init__.py',
 '../tact/dev/test_tact.py',
 '../tact/ntanh/ParamsBase.py',
 '../tact/ntanh/__init__.py']
```

Ví dụ 2: tạo file tham số:

```python

from pprint import pprint
from ntanh.ParamsBase import tactParametters

class Parameters(tactParametters):
    def __init__(self, ModuleName="TACT"):
        super().__init__()
        self.thamso1 = "thamso1"
        self.thamso2 = " xâu tiếng việt"
        self.api_url = "https://200.168.90.38:6699/avi/collect_data"
        self.testpath = "D:/test_debug_fii"
        self.test_real = 0.8
        self.test_int = 12
        self.test_dict = {
            1: 2,
            3: 4.5,
            "6": "bảy nhá",
            -1: "Tám",
            9: [10, 11.2, "22", (33, 44, "55")],
            10: {101: 12, 102: "mười ba"},
        }
        self.test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.load_then_save_to_yaml(file_path="configs_test.yml", ModuleName=ModuleName)
        self.privateVar1 = 2
        self.privateVar2 = "Not in param file"


mParams = Parameters(ModuleName="test")

pprint(mParams.__dict__)
```

Kết quả:

```
{'ModuleName': 'test',
 'api_url': 'https://200.168.90.38:6699/avi/collect_data',
 'fn': 'configs_test.yml',
 'logdir': '',
 'privateVar1': 2,
 'privateVar2': 'Not in param file',
 'test_dict': {-1: 'Tám',
               1: 2,
               3: 4.5,
               9: [10, 11.2, '22', (33, 44, '55')],
               10: {101: 12, 102: 'mười ba'},
               '6': 'bảy nhá'},
 'test_int': 12,
 'test_list': [1, 2, 3, 4, 5, 6, 7, 8, 9],
 'test_real': 0.8,
 'testpath': 'D:/test_debug_fii',
 'thamso1': 'thamso1',
 'thamso2': ' xâu tiếng việt'}
```



          """
    )
