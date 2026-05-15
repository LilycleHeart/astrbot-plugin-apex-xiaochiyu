# 小赤羽 — Apex Legends QQ Bot 插件

<<<<<<< Updated upstream
AstrBot 插件 — Apex Legends 多功能 Bot。

[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.24-blue)](https://astrbot.app)
=======
<p align="center">
  <img src="https://count.getloli.com/@apex-xiaochiyu?theme=rule34&name=apex-xiaochiyu" alt="Moe Counter" />
</p>

基于 AstrBot 的 Apex Legends 多功能插件，支持战绩查询、地图轮换、服务器状态、大师猎杀数据、组队系统，以及 LLM 自然语言交互。
>>>>>>> Stashed changes

## 功能

| 指令 | 别名 | 说明 |
|---|---|---|
| `/stats [玩家名/UID]` | `战绩` `查询` | 查询 Apex 战绩，生成 Material Design 卡片 |
| `/bind <玩家名> [平台]` | `绑定` | 绑定 Apex 账号 |
| `/bind_uid <UID> [平台]` | `绑定UID` | 直接通过 UID 绑定（名字查不到时使用） |
| `/unbind` | `解绑` | 解绑 Apex 账号 |
| `/map` | `地图` | 地图轮换（匹配/排位/限时） |
| `/server` | `服务器` | Apex 服务器状态 |
| `/master` | `大师` | 各平台猎杀线分数和大师人数 |
| `/team create/join/leave/info/list/disband/ttl` | | 组队系统 |

### LLM 自然语言

配置 LLM 后（DeepSeek / OpenAI 等），Bot 自动理解自然语言：

- `看看我的战绩` `查一下数据` → 查询战绩
- `绑定我的账号 Liliumcordis` → 绑定账号
- `现在什么地图` `地图轮换` → 地图轮换
- `服务器炸了吗` → 服务器状态
- `大师多少个` `猎杀线多少分` → 大师数据

LLM 会先评论数据内容，然后自动发送卡片图片。

### 战绩卡片

每张卡片展示：
- 玩家头像、等级、在线状态、平台
- 段位（白金3 格式）、RP 分数、RP 变动（距上次查询）
- 生涯击杀、总伤害、BR 胜场
- 段位分布参考（实时数据，仅显示附近 4 个段位）
- 常用英雄 TOP3
- 赛季徽章

### 地图卡片

带 EA 官方地图背景图，实时显示匹配/排位当前图和下一张，支持地图名汉化。

### 大师数据卡片

Moe Counter (rule34) 数字风格展示四平台猎杀线和大师人数。

## 安装

1. 下载 `astrbot-plugin-apex-xiaochiyu.zip`
2. 在 AstrBot 面板上传安装
3. 配置 `apex_api_key`（[apexlegendsapi.com](https://apexlegendsapi.com) 注册获取）

## 依赖

| 包 | 用途 |
|---|---|
| `httpx>=0.28.0` | API HTTP 请求 |
| `aiosqlite>=0.20.0` | SQLite 异步数据库 |
| `Pillow>=10.0.0` | 图片渲染回退方案 |
| `playwright>=1.48.0` | HTML→PNG 卡片渲染 |

> 安装后需执行 `python -m playwright install webkit` 下载 WebKit 浏览器内核。
| `mcp>=1.20.0` | LLM 工具 CallToolResult 类型 |

## 配置

```json
{
  "apex_api_key": "你的 API Key"
}
```

API Key 在 [apexlegendsapi.com](https://portal.apexlegendsapi.com) 免费注册。

## 项目结构

```
├── main.py                    # 插件入口，指令和 LLM 工具
├── libs/
│   ├── apex_client.py         # API 封装层
│   ├── playwright_renderer.py # 卡片 HTML 模板和渲染
│   ├── image_renderer.py      # Pillow 回退渲染
│   ├── als_scraper.py         # ALS 网站徽章抓取
│   ├── database.py            # SQLite 数据库层
│   ├── playwright_manager.py  # 共享浏览器管理器
│   ├── http_client.py         # 共享 HTTP 连接池
│   ├── ttl_cache.py           # TTL 内存缓存
│   └── config.py              # Material Design 配色
└── assets/
    └── fonts/                 # 字体文件
```

## 鸣谢

- 数据来源：[Apex Legends Status](https://apexlegendsstatus.com) / [ApexLegendsAPI](https://apexlegendsapi.com)
- Moe Counter 数字：[journey-ad/Moe-Counter](https://github.com/journey-ad/Moe-Counter)
- 地图背景：[EA Apex Legends Maps Hub](https://www.ea.com/zh-hant/games/apex-legends/apex-legends/game-objects/maps-hub)
