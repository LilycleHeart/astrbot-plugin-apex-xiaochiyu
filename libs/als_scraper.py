"""ALS 网站徽章抓取器 / 名字搜索"""

from __future__ import annotations

from .playwright_manager import run_with_page


async def _do_fetch(page, name_or_uid: str, platform: str) -> dict:
    url = f"https://apexlegendsstatus.com/profile/{platform}/{name_or_uid}"
    await page.goto(url, wait_until="load", timeout=30000)
    await page.wait_for_timeout(4000)
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
    """在 ALS 网站搜索玩家名，返回匹配列表 [{name, uid, platform}]"""
    from urllib.parse import quote

    url = f"https://apexlegendsstatus.com/profile/{platform}/{quote(name)}"
    async with run_with_page() as page:
        try:
            await page.goto(url, wait_until="load", timeout=30000)
            await page.wait_for_timeout(3000)
            # ALS 不存在的玩家会显示搜索页/错误页
            results = await page.evaluate("""() => {
                const items = [];
                // 尝试从搜索结果列表提取
                document.querySelectorAll('.search-results a, .v2-player-result, [class*="player"] a').forEach(el => {
                    const uid = (el.href || '').match(/uid\\/(\\w+)\\/(\\d+)/);
                    if (uid) items.push({name: el.textContent.trim(), uid: uid[2], platform: uid[1]});
                });
                // 如果当前页就是玩家页（直接命中）
                if (!items.length) {
                    const name = (document.querySelector('.player-name') || {}).textContent?.trim();
                    const puid = (document.getElementById('puid') || {}).value;
                    if (name && puid) items.push({name, uid: puid, platform: 'PC'});
                }
                return items.slice(0, 10);
            }""")
            return results
        except Exception as e:
            from astrbot.api import logger
            logger.error(f"[SearchPlayers] Error: {e}")
            return []
