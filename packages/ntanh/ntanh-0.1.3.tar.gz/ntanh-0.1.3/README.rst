# Giới thiệu

ntanh là một thư viện các nhiệm vụ hàng ngày sử dụng, hay dùng nhưng không khó, mất thời gian code cho các dự án lẻ tẻ.

# Cài đặt
`pip install tact`

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





