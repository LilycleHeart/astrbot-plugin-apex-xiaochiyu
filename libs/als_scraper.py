"""ALS 网站徽章抓取器 / 名字搜索"""

from __future__ import annotations

from .playwright_manager import run_with_page


async def _do_fetch(page, name_or_uid: str, platform: str) -> dict:
    url = f"https://apexlegendsstatus.com/profile/{platform}/{name_or_uid}"
    await page.goto(url, wait_until="networkidle", timeout=30000)
    return await page.evaluate("""() => {
        const colors = {
            bronze:'#cd7f32',silver:'#c0c0c0',gold:'#ffd700',
            platinum:'#4ECDC4',diamond:'#358de6',
            master:'#9f35e6',predator:'#e31b39'
        };
        const seasons = [];
        document.querySelectorAll('img[src*="you_re_tiering_me_apart"]').forEach(img => {
            const m = img.src.match(/you_re_tiering_me_apart_(\\w+)_rs(\\d+)/);
            if (m) seasons.push({
                season: 'S' + m[2],
                tier: m[1],
                badge_url: img.src,
                color: colors[m[1]] || '#666'
            });
        });
        const special = [];
        const seen = new Set();
        document.querySelectorAll('img[src*="badges"]').forEach(img => {
            const src = img.src;
            if (src.includes('you_re_tiering_me_apart')) return;
            const m = src.match(/badges\\/badges_new\\/(.+?)\\.png/);
            if (m) {
                let nm = m[1].replace(/_/g,' ').replace(/\\b\\w/g,c=>c.toUpperCase());
                nm = nm.replace(/ Rs\\d+/,'')
                       .replace(/ Iv$/,' IV').replace(/ Iii$/,' III')
                       .replace(/ Ii$/,' II').replace(/ Vi$/,' VI');
                if (!seen.has(nm) && nm.length < 40) {
                    seen.add(nm);
                    special.push({name:nm, color:'#b1f4fa'});
                }
            }
        });
        const text = document.body.innerText;
        const gIdx = text.indexOf('\\nGlobal\\n');
        let kills = 0;
        if (gIdx >= 0) {
            const gSection = text.substring(gIdx, gIdx + 500);
            const ck = gSection.match(/Career Kills\\s*\\n([\\d,]+)\\n/);
            if (ck) kills = parseInt(ck[1].replace(/,/g,''));
        }
        let level = 0, prestige = 0;
        const lv = text.match(/LEVEL\\s*\\n(\\d+)\\s*\\nPRESTIGE\\s*(\\d+)/);
        if (lv) { level = parseInt(lv[1]); prestige = parseInt(lv[2]); }
        return {seasons, special: special.slice(0, 5), kills, level, prestige};
    }""")


async def fetch_badges(name_or_uid: str, platform: str = "PC") -> dict:
    """从 ALS 个人页面抓取赛季徽章和特殊徽章，空数据自动重试一次"""
    from astrbot.api import logger

    for attempt in range(2):
        try:
            async with run_with_page() as page:
                result = await _do_fetch(page, name_or_uid, platform)
                if result.get("seasons") or result.get("kills"):
                    return result
                if attempt == 0:
                    logger.warning(f"[BadgeFetcher] 数据为空，重试... {name_or_uid}")
        except Exception as e:
            if attempt == 0:
                logger.warning(f"[BadgeFetcher] 失败，重试... {e}")
            else:
                logger.error(f"[BadgeFetcher] Error: {e}")

    return {"seasons": [], "special": []}


async def search_players(name: str, platform: str = "PC") -> list[dict]:
    """访问ALS玩家页面，从DOM提取数据"""
    encoded = name.replace("+", "%2B").replace(" ", "+")
    url = f"https://apexlegendsstatus.com/profile/{platform}/{encoded}"
    async with run_with_page() as page:
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            from astrbot.api import logger
            logger.info(f"[SearchPlayers] 实际URL: {page.url} (请求: {url})")
            # 截图存 debug_screenshots/
            import uuid, os
            debug_dir = os.path.join(os.path.dirname(__file__), "..", "debug_screenshots")
            os.makedirs(debug_dir, exist_ok=True)
            safe_name = name.replace(" ", "_").replace("/", "_")[:30]
            await page.screenshot(path=os.path.join(debug_dir, f"search_{safe_name}.png"), full_page=True)
            try:
                await page.wait_for_selector(".player-name", timeout=10000)
            except Exception:
                pass
            result = await page.evaluate("""() => {
                const items = [];
                // 1. 搜索页: 找所有玩家链接 (href含profile/uid)
                document.querySelectorAll('a[href*="profile/uid"]').forEach(a => {
                    const m = (a.href || '').match(/profile\\/uid\\/(\\w+)\\/(\\d+)/);
                    if (m) items.push({name: a.textContent.trim(), uid: m[2], platform: m[1]});
                });
                // 2. 搜索页: 找 .search-result 行
                document.querySelectorAll('.search-result, .player-search-result, [class*="search"] a[href*="/profile/"]').forEach(a => {
                    const m = (a.href || '').match(/profile\\/(?:uid\\/)?(\\w+)\\/(\\d+)/);
                    if (m && !items.find(i => i.uid === m[2])) {
                        items.push({name: a.textContent.trim(), uid: m[2], platform: m[1]});
                    }
                });
                // 3. 如果是直接玩家页
                if (!items.length) {
                    const name = (document.querySelector('.player-name') || {}).textContent?.trim();
                    const uid = (document.getElementById('puid') || {}).value;
                    if (name && uid) items.push({name, uid, platform: '""" + platform + """'});
                }
                // 去重
                const seen = new Set();
                return items.filter(i => { const k = i.uid; if (seen.has(k)) return false; seen.add(k); return true; }).slice(0, 10);
            }""")
            return result
        except Exception as e:
            from astrbot.api import logger
            logger.error(f"[SearchPlayers] Error: {e}")
            return []
