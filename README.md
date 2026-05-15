# 小赤羽 / Astrobot Apex数据查询插件

<p align="center">
  <img src="https://count.getloli.com/get/@LilycleHeart-astrbot-plugin-apex-xiaochiyu?theme=rule34" alt="Moe Counter" /><br>
  <a href="https://github.com/LilycleHeart/astrbot-plugin-apex-xiaochiyu">
    <img src="https://img.shields.io/github/stars/LilycleHeart/astrbot-plugin-apex-xiaochiyu?style=social" alt="GitHub stars">
  </a>
</p>

AstrBot 插件 — Apex Legends 多功能 Bot。

[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.24-blue)](https://astrbot.app)

## 功能

| 指令 | 说明 |
|---|---|
| `/stats [玩家名]` | 查询战绩，生成卡片数据 |
| `/bind <玩家名> [PC/PS4/X1]` | 绑定 Apex 账号 |
| `/bind_uid <UID> [平台]` | 直接通过 UID 绑定 |
| `/unbind` | 解绑账号 |
| `/map` | 地图轮换（匹配 / 排位 / 限时模式） |
| `/server` | Apex 服务器状态 |
| `/master` | 各平台猎杀分数线线 + 大师（猎杀）总人数 |
| `/team ...` | 组队系统 |

配置 LLM 后支持自然语言：`看看我的战绩` `服务器炸了吗` `现在什么地图` `大师多少个` — Bot 自动识别意图，先评论数据再发卡片。

### 战绩卡片

- 玩家信息、段位（白金3 格式）、RP 分数及变动
- 生涯击杀 / 总伤害 / BR 胜场
- 段位分布参考（实时数据，仅显示附近 4 个段位）
- 常用英雄 TOP3、赛季徽章、当前选用

### 地图卡片

带 EA 官方地图背景图，中文地图名，实时倒计时。

### 大师数据卡片

Moe Counter (rule34) 数字风格，四平台猎杀分数线 + 大师人数。

## 安装

在 AstrBot WebUI → 插件管理 → 上传 `astrbot-plugin-apex-xiaochiyu.zip`
或在Astrobot插件市场添加

## 配置

```json
{
  "apex_api_key": "YOUR_KEY"
}
```

API Key 在 [apexlegendsapi.com](https://portal.apexlegendsapi.com) 免费注册。

## 依赖

| 包 | 用途 |
|---|---|
| `httpx>=0.28.0` | API HTTP 请求 |
| `aiosqlite>=0.20.0` | SQLite 异步数据库 |
| `Pillow>=10.0.0` | 图片渲染回退方案 |
| `playwright>=1.48.0` | HTML→PNG 卡片渲染 |
| `mcp>=1.20.0` | LLM 工具返回值类型 |

> 安装后需执行 `python -m playwright install webkit` 下载 WebKit 内核。

## 数据来源

- 战绩 / 地图 / 服务器：[Apex Legends Status](https://apexlegendsstatus.com)
- Moe Counter 数字：[journey-ad/Moe-Counter](https://github.com/journey-ad/Moe-Counter)
- 地图背景：[EA Apex Maps Hub](https://www.ea.com/zh-hant/games/apex-legends/apex-legends/game-objects/maps-hub)
