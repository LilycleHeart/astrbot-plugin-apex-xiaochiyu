```markdown
<p align="center">
  <img src="https://capsule-render.github.io/api?type=rounded&text=小赤羽%20/%20AstrBot%20Apex&color=6750A4&fontColor=ffffff&height=140&fontSize=48" width="100%" alt="Header" />
</p>

<p align="center">
  <a href="https://astrbot.app">
    <img src="https://img.shields.io/badge/AstrBot-%3E%3D4.24-6750A4?style=for-the-badge&logo=android" alt="AstrBot Version" />
  </a>
  <img src="https://count.getloli.com/get/@xiaochiyu-apex-bot?theme=rule34" height="28" alt="Moe Counter" />
</p>

<p align="center">
  🪐 <b>AstrBot 插件 — 一款优雅、全能的 Apex Legends 数据查询助理</b>
</p>

---

<table width="100%" style="border-collapse: collapse; border: none; margin-bottom: 24px;">
  <tr style="background-color: #F3EDF7; border: none;">
    <td style="padding: 20px; border-radius: 16px; border: none; color: #1D1B20;">
      <h4 style="margin: 0 0 8px 0; font-size: 16px; display: flex; align-items: center; gap: 8px;">
        🤖 <b>Material 3 智能语义驱动</b>
      </h4>
      <p style="margin: 0; font-size: 14px; color: #49454F; line-height: 1.6;">
        配置 LLM（大语言模型）后，Bot 将完美支持自然语言交互。无论是 <i>“看看我的战绩”</i>、<i>“服务器炸了吗”</i> 还是 <i>“现在什么地图”</i>，Bot 都能自动识别意图，<b>先以拟人化口吻评论数据，再呈递精致的卡片</b>。
      </p>
    </td>
  </tr>
</table>

## 🛠️ 功能特性

### 🎯 核心指令

| 指令 | 说明 |
| :--- | :--- |
| `/stats [玩家名]` | 查询战绩，生成卡片数据 |
| `/bind <玩家名> [PC/PS4/X1]` | 绑定 Apex 账号 |
| `/bind_uid <UID> [平台]` | 直接通过 UID 绑定 |
| `/unbind` | 解绑账号 |
| `/map` | 地图轮换（匹配 / 排位 / 限时模式） |
| `/server` | Apex 服务器状态 |
| `/master` | 各平台猎杀分数线线 + 大师（猎杀）总人数 |
| `/team ...` | 组队系统 |

---

### 🎨 视觉卡片设计

* **📊 战绩卡片**
  * 完整展示玩家信息、段位（白金3 格式）、RP 分数及实时变动。
  * 生涯击杀、总伤害、BR 胜场等核心数据一目了然。
  * 内置段位分布参考（实时数据，仅显示附近 4 个段位）。
  * 追踪常用英雄 TOP3、赛季徽章及当前选用皮肤。
* **🗺️ 地图卡片**
  * 适配 EA 官方最新的地图背景图，采用全中文地图名，附带精确的实时倒计时。
* **👑 大师数据卡片**
  * 融合 `Moe Counter (rule34)` 数字风格，实时监控四大平台猎杀分数线与大师总人数。

---

## 🚀 快速安装

1. 进入 **AstrBot WebUI** → **插件管理**。
2. 点击 **上传插件**，选择 `astrbot-plugin-apex-xiaochiyu.zip` 进行上传；或者直接在 **AstrBot 插件市场** 搜索添加。
3. > ⚠️ **重要依赖环境**：安装完成后，必须在系统终端执行以下命令以下载 WebKit 内核：
   ```bash
   python -m playwright install webkit

```

---

## ⚙️ 插件配置

在插件配置面板中填入你的 API Key：

```json
{
  "apex_api_key": "YOUR_KEY"
}

```

> 💡 **API Key 获取方式**：可在 [apexlegendsapi.com](https://portal.apexlegendsapi.com) 免费注册获取。

---

## 📦 项目依赖

| 依赖包 | 最低版本 | 用途说明 |
| --- | --- | --- |
| `httpx` | `>=0.28.0` | 处理高效的 API HTTP 异步请求 |
| `aiosqlite` | `>=0.20.0` | SQLite 异步数据库本地数据持久化 |
| `Pillow` | `>=10.0.0` | 图片轻量化渲染及回退方案 |
| `playwright` | `>=1.48.0` | 核心引擎：将 HTML 异步渲染为高保真 PNG 卡片 |
| `mcp` | `>=1.20.0` | 标准化 LLM 工具返回值类型 |

---

## 🌐 数据来源与致谢

本插件的高效运行离不开以下优秀公开服务与开源项目的支持：

* **战绩 / 地图 / 服务器数据**：[Apex Legends Status](https://apexlegendsstatus.com)
* **Moe Counter 经典数字**：[journey-ad/Moe-Counter](https://github.com/journey-ad/Moe-Counter)
* **精美地图背景**：[EA Apex Maps Hub](https://www.ea.com/zh-hant/games/apex-legends/apex-legends/game-objects/maps-hub)

```

```
