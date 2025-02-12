# Money Analyze

[🇬🇧 English](README.en.md) | [🇹🇼 繁體中文](README.zh-TW.md)

## 📌 專案介紹

**Money Analyze** 是一款以台灣法律為基礎的金融計算工具，旨在評估 **房屋增貸投資股票** 並以 **賣股還款** 的潛在收益與風險。此外，若將相關費用設定為 **0 元**，本工具亦可模擬 **將月薪投入特定 ETF，並分期提領的效果**，而年利率可視作通膨率。

---

## 📊 **模擬條件與參數**

- **投資標的**：假設年化報酬率 **15%**，年化標準差 **20%**
- **增貸金額**：新台幣 **100 萬**
- **手續費與稅金**：
  - **增貸內扣費用**：0.6%
  - **股票手續費**：0.1425%（假設手續費享 **6 折** 優惠）
  - **交易稅**：0.1%（ETF 按原價計算）
  - **總增貸手續成本**：5300 元
- **實際可投資金額**：99.47 萬元
- **貸款年利率**：3.2%

---

## 💰 **收益與風險評估**

### 📆 **短期還款方案**（84 期）

- **月繳金額**：13,303 元
- **預期收益**：805,214 元（**+80%**）
- **虧損機率**：**17%**（模擬 100,000 次，虧損 16,440 次）

### 📆 **長期還款方案**（240 期）

- **月繳金額**：5,646 元
- **預期收益**：9,828,859 元（**+980%**）
- **虧損機率**：**6%**（模擬 100,000 次，虧損 5,314 次）

### 📆 **短期月薪投資方案**（84 期）( no related fee )

- **月領金額**：13,303 元
- **預期收益**：824,228 元（**+82%**）
- **虧損機率**：**16%**（模擬 100,000 次，虧損 15,920 次）

### 📆 **長期月薪投資方案**（240 期）( no related fee )

- **月領金額**：5,646 元
- **預期收益**：9,945,344 元（**+990%**）
- **虧損機率**：**6%**（模擬 100,000 次，虧損 5,280 次）

---

## 📝 **結論**

1. **短期還款方案（84 期）**：月繳金額較高，但風險相對較小，預期收益約 **180%**，虧損機率 **17%**。
2. **長期還款方案（240 期）**：月繳金額較低，累積時間較長，預期收益顯著提高至 **1080%**，虧損機率下降至 **6%**。
3. **關鍵風險因素**：標的波動性（年化標準差 20%）將影響實際收益，投資者需根據自身風險承受能力選擇適合的方案。

🔹 **投資有風險，請審慎評估自身財務狀況與風險承受度！**
