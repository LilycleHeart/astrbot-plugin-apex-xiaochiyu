# 小赤羽 / AstrBot Apex 数据查询插件

AstrBot 插件 —— 一个专注于 Apex英雄数据查询、组队与状态追踪的多功能 Bot。
<p align="center">
  <img src="https://count.getloli.com/@apex-xiaochiyu?theme=rule34&name=apex-xiaochiyu" alt="Moe Counter" />
</p>

[![AstrBot](https://img.shields.io/badge/AstrBot-%3E%3D4.24-blue)](https://astrbot.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)](https://www.python.org/)
[![License](https://img.shields.io/github/license/LilycleHeart/astrbot-plugin-apex-xiaochiyu)](https://github.com/LilycleHeart/astrbot-plugin-apex-xiaochiyu)

---

## ✨ 功能特性

### 📊 战绩查询

查询玩家实时数据，并生成高质量战绩卡片：

- 当前段位、RP 分数、分数变动
- 生涯击杀 / 总伤害 / BR 胜场
- 常用英雄 TOP3
- 当前赛季徽章
- 附近段位分布参考
- 当前选用传奇角色

### 🗺️ 地图轮换

实时获取：

- 匹配地图
- 排位地图
- 限时模式地图
- 剩余轮换时间

并自动生成带官方背景图的地图卡片。

### 🌐 服务器状态

快速查看：

- EA 服务器状态
- 数据中心在线情况
- 是否存在异常或炸服

### 👑 猎杀 / 大师数据

提供：

- 四平台猎杀分数线
- 大师 / 猎杀人数统计
- Moe Counter 风格数字卡片

### 👥 组队系统

支持简单队伍管理：

- 创建队伍
- 加入 / 退出队伍
- 队伍状态同步

### 🤖 LLM 自然语言支持

配置 LLM 后，可直接使用自然语言触发功能：

```text
看看我的战绩
现在什么地图
服务器炸了吗
大师多少分了
```

Bot 会自动识别意图，优先返回文字总结，再发送数据卡片。

---

## 📖 指令列表

| 指令 | 说明 |
|---|---|
| `/stats [玩家名]` | 查询玩家战绩 |
| `/bind <玩家名> [PC/PS4/X1]` | 绑定 Apex 账号 |
| `/bind_uid <UID> [平台]` | 使用 UID 绑定 |
| `/unbind` | 解绑账号 |
| `/map` | 查看地图轮换 |
| `/server` | 查看服务器状态 |
| `/master` | 查看猎杀分数线与大师人数 |
| `/team ...` | 组队系统 |

---

## 🖼️ 卡片展示

### 战绩卡片

- 玩家基础信息
- 段位 / RP
- 生涯数据
- 英雄数据
- 徽章展示
- 段位分布参考

### 地图卡片

- 官方地图背景
- 中文地图名
- 实时倒计时

### 大师数据卡片

- Moe Counter 数字风格
- 四平台猎杀线
- 大师人数统计

---

## 📦 安装

### 方法一：插件市场安装

在 AstrBot 插件市场搜索：

```text
小赤羽
```

### 方法二：手动安装

下载仓库 ZIP：

```text
astrbot-plugin-apex-xiaochiyu.zip
```

然后在 AstrBot WebUI：

```text
插件管理 → 上传插件
```

---

## ⚙️ 配置

```json
{
  "apex_api_key": "YOUR_API_KEY"
}
```

API Key 免费获取：

- https://portal.apexlegendsapi.com

---

## 🔧 依赖

| 包 | 用途 |
|---|---|
| `httpx>=0.28.0` | HTTP API 请求 |
| `aiosqlite>=0.20.0` | SQLite 异步数据库 |
| `Pillow>=10.0.0` | 图片渲染回退 |
| `playwright>=1.48.0` | HTML → PNG 卡片渲染 |
| `mcp>=1.20.0` | LLM 工具返回值类型 |

安装依赖后，还需要安装 WebKit：

```bash
python -m playwright install webkit
```

---

## 📚 数据来源

- 战绩 / 地图 / 服务器  
  https://apexlegendsstatus.com

- Moe Counter 数字样式  
  https://github.com/journey-ad/Moe-Counter

- 地图背景资源  
  https://www.ea.com/zh-hant/games/apex-legends/apex-legends/game-objects/maps-hub

---

## ⭐ Star 支持

如果这个插件对你有帮助，欢迎点个 Star 支持一下项目。
