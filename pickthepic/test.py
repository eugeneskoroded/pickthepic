import requests
import base64
import scipy.stats as sp
import numpy as np

def conv_interval(n_views, n_conv, alpha=0.95):
    x = [1 for i in range(n_conv)]
    x.extend([0 for i in range(n_views - n_conv)])
    x_mean = np.mean(x)
    d = np.var(x, ddof=1) * n_views / (n_views - 1)
    step = sp.t.ppf((alpha + 1) / 2, n_views - 1) * np.sqrt(d / n_views)
    interval = [x_mean - step, x_mean + step]
    return interval
print(conv_interval(2, 1))
# key_imgbb = '24b9c134a36f15aee02b36285d79b9c5'
# with open("./media/images/cat.jpg", "rb") as file:
#     url = "https://api.imgbb.com/1/upload"
#     payload = {
#         "key": key_imgbb,
#         "image": base64.b64encode(file.read()),
#     }
#     res = requests.post(url, payload)
# print(res.json()['data']['medium']['url'])

# for i in range(10):
#     l = np.random.choice(['A', 'B'], p=[0.5, 0.5])
#     print(l)