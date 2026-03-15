# A股免费行情 API 汇总

> 来源：知乎文章 + 公开资料整理
> 更新：2026-03-15

---

## 1. 新浪财经 API（推荐）

### 特点
- ✅ 完全免费，无需注册
- ✅ 实时数据
- ✅ 稳定性好
- ✅ 支持 A股、港股、美股

### 接口示例

#### 获取实时行情
```
https://hq.sinajs.cn/list=sh600000,sz000001
```

返回格式（JavaScript变量）：
```javascript
var hq_str_sh600000="浦发银行,10.50,10.48,10.52,10.55,10.48,10.51,10.52,1234567,13000000,10.51,1000,10.52,2000,...";
```

字段说明：
- 0: 股票名称
- 1: 今日开盘价
- 2: 昨日收盘价
- 3: 当前价格
- 4: 今日最高价
- 5: 今日最低价
- 6-7: 买一/卖一价
- 8: 成交量（股）
- 9: 成交金额（元）

#### 获取分时数据
```
https://quotes.sina.cn/cn/api/quotes.php?symbol=sh600000&dpc=1
```

#### 获取 K线数据
```
https://stock.finance.sina.com.cn/stock/api/jsonp.php/var_KL_Services.getHistoricData=/Service/CentreDal.getStockKLine?symbol=sh600000&period=day
```

---

## 2. 腾讯财经 API

### 特点
- ✅ 免费，无需注册
- ✅ 数据格式简洁（JSON）
- ✅ 支持批量查询

### 接口示例

#### 实时行情
```
https://qt.gtimg.cn/q=sh600000,sz000001
```

返回格式：
```
v_sh600000="1~浦发银行~600000~10.52~10.48~10.50~1234567~13000000~...";
```

#### 详细数据
```
https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600000,day,2024-01-01,2024-12-31,500,qfq
```

---

## 3. 东方财富 API

### 特点
- ✅ 数据全面
- ✅ 支持资金流向
- ⚠️ 部分接口需要 Cookie

### 接口示例

#### 实时行情
```
https://push2.eastmoney.com/api/qt/stock/get?secid=1.600000&fields=f43,f44,f45,f46,f47,f48,f57,f58
```

返回格式：JSON

#### 资金流向
```
https://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=1.600000
```

---

## 4. 同花顺 API

### 特点
- ✅ 数据实时
- ⚠️ 部分接口需要登录

### 接口示例
```
http://d.10jqka.com.cn/v4/line/hs_600000/01/last.js
```

---

## 5. 雪球 API

### 特点
- ✅ 社区数据丰富
- ⚠️ 需要 Cookie

### 接口示例
```
https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol=SH600000
```

---

## 6. 网易财经 API

### 特点
- ✅ 历史数据完整
- ✅ 支持复权数据

### 接口示例

#### 历史 K线
```
http://quotes.money.163.com/service/chddata.html?code=0600000&start=20240101&end=20241231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
```

---

## 推荐方案

### 实时行情
| 优先级 | 数据源 | 用途 |
|-------|-------|------|
| 1 | 新浪财经 | 实时价格、涨跌幅 |
| 2 | 腾讯财经 | 备用/批量查询 |
| 3 | 东方财富 | 资金流向 |

### 历史数据
| 优先级 | 数据源 | 用途 |
|-------|-------|------|
| 1 | 网易财经 | K线数据、复权 |
| 2 | 新浪财经 | 分时数据 |

### 竞价数据（09:25-09:30）
| 优先级 | 数据源 | 用途 |
|-------|-------|------|
| 1 | 新浪财经 | 集合竞价 |
| 2 | 东方财富 | 竞价明细 |

---

## 使用示例代码

### Python 获取实时行情
```python
import requests

def get_sina_quote(stock_codes):
    """
    获取新浪财经实时行情
    stock_codes: ['sh600000', 'sz000001']
    """
    url = f"https://hq.sinajs.cn/list={','.join(stock_codes)}"
    headers = {
        'Referer': 'https://finance.sina.com.cn',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    # 解析返回数据...
    return response.text

def get_qq_quote(stock_codes):
    """
    获取腾讯财经实时行情
    stock_codes: ['sh600000', 'sz000001']
    """
    codes = [c.replace('sh', 'sh').replace('sz', 'sz') for c in stock_codes]
    url = f"https://qt.gtimg.cn/q={','.join(codes)}"
    response = requests.get(url)
    return response.text
```

---

## 注意事项

1. **频率限制**：免费接口通常有访问频率限制，建议加延迟
2. **Referer 头**：部分接口需要设置 Referer
3. **编码问题**：注意返回数据的编码（通常是 GBK/GB2312）
4. **备用方案**：建议同时配置多个数据源，互为备份

---

## 下一步

1. 封装统一的数据获取接口
2. 实现 09:00/09:30/11:30/15:00 数据抓取
3. 缓存机制（避免重复请求）
4. 异常处理和备用切换
