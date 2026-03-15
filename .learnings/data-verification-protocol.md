# 数据正确性验证协议

> 严格执行，无例外

---

## 🚨 核心原则

**任何数据输出前，必须通过以下验证流程。**

**违反后果**：数据错误会直接导致经济损失和信任崩塌。

---

## 📋 股票数据验证流程

### 第一步：代码核实

```python
# 必须验证：代码 ↔ 名称 匹配
def verify_stock_identity(code, name):
    """
    验证股票代码和名称匹配
    """
    # 1. 从智途API获取全市场列表
    # 2. 查询代码对应的名称
    # 3. 确认与输入名称一致
    # 4. 不一致 → 拒绝输出，重新查询
```

**检查点**：
- [ ] 代码格式正确（6位数字）
- [ ] 代码存在且有效
- [ ] 代码与名称匹配

### 第二步：价格核实

```python
# 必须验证：价格实时性
def verify_price_realtime(code):
    """
    获取并验证实时价格
    """
    # 1. 调用腾讯财经API获取实时行情
    # 2. 记录查询时间戳
    # 3. 返回完整价格数据
```

**检查点**：
- [ ] 价格来自实时API
- [ ] 时间戳在5分钟内
- [ ] 价格数据完整（开/高/低/收/现）

### 第三步：交叉验证

```python
# 必须验证：多源交叉确认
def cross_verify_price(code):
    """
    多数据源交叉验证
    """
    # 1. 腾讯财经API
    # 2. 新浪财经API
    # 3. 两者价格差异 < 1%
    # 4. 差异过大 → 标记异常，人工复核
```

**检查点**：
- [ ] 至少2个数据源
- [ ] 价格差异 < 1%
- [ ] 异常数据标记并拒绝输出

### 第四步：输出前最终检查

```python
# 必须验证：输出格式检查
def final_output_check(stock_data):
    """
    输出前最终验证
    """
    checks = {
        '代码': len(stock_data['code']) == 6,
        '名称': stock_data['name'] and len(stock_data['name']) >= 2,
        '价格': stock_data['price'] > 0 and stock_data['price'] < 10000,
        '涨跌幅': -30 < stock_data['change_pct'] < 30,
        '时间戳': stock_data['timestamp'] within 5 minutes
    }
    
    # 任何检查失败 → 拒绝输出
    if not all(checks.values()):
        raise DataVerificationError("验证失败，拒绝输出")
```

---

## 🔒 强制执行规则

### 规则1：无验证，不输出

- 任何股票数据必须通过全部4步验证
- 验证失败 → 明确告知"数据验证失败，无法提供"
- 绝不输出未经核实的数据

### 规则2：异常即停止

- 数据源不一致 → 停止输出，标记异常
- API返回错误 → 停止输出，报告错误
- 价格异常（如涨跌幅>20%）→ 停止输出，人工复核

### 规则3：留痕可追溯

- 每次数据查询记录日志
- 包含：时间、代码、名称、价格、数据源
- 错误数据保留用于复盘

---

## 🛠️ 技术实现

### 验证模块

```python
# scripts/data_verifier.py

class StockDataVerifier:
    """股票数据验证器"""
    
    def __init__(self):
        self.zhitu = ZhituAPI()
        self.stock_api = StockDataAPI()
        self.verification_log = []
    
    def verify(self, code, expected_name=None):
        """
        完整验证流程
        """
        result = {
            'code': code,
            'verified': False,
            'data': None,
            'errors': []
        }
        
        # Step 1: 代码核实
        stock_info = self._verify_code(code)
        if not stock_info:
            result['errors'].append('代码核实失败')
            return result
        
        # Step 2: 名称匹配
        if expected_name and stock_info['name'] != expected_name:
            result['errors'].append(f'名称不匹配: {stock_info["name"]} != {expected_name}')
            return result
        
        # Step 3: 价格核实
        price_data = self._verify_price(code)
        if not price_data:
            result['errors'].append('价格核实失败')
            return result
        
        # Step 4: 交叉验证
        if not self._cross_verify(code, price_data['price']):
            result['errors'].append('交叉验证失败')
            return result
        
        # 全部通过
        result['verified'] = True
        result['data'] = {
            'code': code,
            'name': stock_info['name'],
            'price': price_data['price'],
            'change_pct': price_data['change_pct'],
            'timestamp': datetime.now(),
            'sources': ['zhitu', 'tencent', 'sina']
        }
        
        self._log_verification(result)
        return result
    
    def _verify_code(self, code):
        """验证代码存在性和名称"""
        # 实现代码...
        pass
    
    def _verify_price(self, code):
        """验证价格实时性"""
        # 实现代码...
        pass
    
    def _cross_verify(self, code, price):
        """交叉验证价格"""
        # 实现代码...
        pass
    
    def _log_verification(self, result):
        """记录验证日志"""
        self.verification_log.append({
            'time': datetime.now().isoformat(),
            'result': result
        })
```

### 使用示例

```python
# 任何股票数据输出前
verifier = StockDataVerifier()

# 验证中国核电
result = verifier.verify('601985', expected_name='中国核电')

if result['verified']:
    # 只有通过验证才能输出
    data = result['data']
    print(f"{data['code']} {data['name']}: ¥{data['price']}")
else:
    # 验证失败，拒绝输出
    print(f"❌ 数据验证失败: {', '.join(result['errors'])}")
    print("⚠️ 无法提供该股票数据，请稍后重试")
```

---

## 📊 验证检查表

每次输出股票数据前，必须勾选：

```markdown
- [ ] 代码格式正确（6位数字）
- [ ] 代码存在于市场
- [ ] 代码与名称匹配
- [ ] 价格来自实时API
- [ ] 时间戳在5分钟内
- [ ] 多源价格差异<1%
- [ ] 价格在合理范围（>0, <10000）
- [ ] 涨跌幅在合理范围（-30%~+30%）
- [ ] 已记录验证日志
```

**全部勾选完成 → 方可输出**

---

## 🎯 执行承诺

1. **严格执行上述流程，无例外**
2. **验证失败时明确告知，不猜测输出**
3. **每次错误后复盘，完善检查点**
4. **定期审计验证日志，发现系统性问题**

---

*建立时间: 2026-03-15*  
*执行人: 二郎*  
*监督人: 楷楷*
