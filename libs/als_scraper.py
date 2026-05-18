"""ALS 网站徽章抓取器 / 名字搜索"""

from __future__ import annotations

from urllib.parse import quote

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from .playwright_manager import run_with_page


async def _block_noise(page):
    """拦截图片/字体/媒体/统计请求，加速页面加载"""
    await page.route(
        "**/*",
        lambda route: route.abort()
        if route.request.resource_type in ("image", "font", "media", "stylesheet")
        or "analytics" in (route.request.url or "")
        or "googletagmanager" in (route.request.url or "")
        or "cookieconsent" in (route.request.url or "")
        else route.continue_(),
    )


async def _do_fetch(page, name_or_uid: str, platform: str) -> dict:
    url = f"https://apexlegendsstatus.com/profile/{platform}/{name_or_uid}"
    await _block_noise(page)
    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    try:
        await page.wait_for_selector(".player-name", timeout=5000)
    except Exception:
        pass
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
    """从 ALS 个人页面抓取赛季徽章和特殊徽章（仅网络超时重试，空数据不重试）"""
    import time
    from astrbot.api import logger
    t0 = time.time()

    for attempt in range(2):
        try:
            async with run_with_page() as page:
                result = await _do_fetch(page, name_or_uid, platform)
                dt = time.time() - t0
                logger.info(f"[BadgeFetcher] 耗时: {dt:.1f}s (attempt={attempt+1})")
                return result
        except PlaywrightTimeoutError:
            if attempt == 0:
                logger.warning(f"[BadgeFetcher] 网络超时，重试... {name_or_uid}")
                continue
            logger.error(f"[BadgeFetcher] 连续超时，放弃 {name_or_uid}")
        except Exception as e:
            if attempt == 0:
                logger.warning(f"[BadgeFetcher] 失败，重试... {e}")
                continue
            logger.error(f"[BadgeFetcher] Error: {e}")
            break

    return {"seasons": [], "special": []}


async def search_players(name: str, platform: str = "PC") -> list[dict]:
    """访问ALS玩家页面，从DOM提取数据"""
    import time
    from astrbot.api import logger
    t0 = time.time()
    encoded = quote(name, safe="")
    url = f"https://apexlegendsstatus.com/profile/{platform}/{encoded}"
    async with run_with_page() as page:
        try:
            await _block_noise(page)
            await page.goto(url, wait_until="commit", timeout=10000)
            logger.info(f"[SearchPlayers] 实际URL: {page.url} (请求: {url})")
            dt = time.time() - t0
            logger.info(f"[SearchPlayers] 页面加载耗时: {dt:.1f}s")
            try:
                await page.wait_for_selector(".player-name", timeout=5000)
            except Exception:
                pass
            result = await page.evaluate("""() => {
                const items = [];
                document.querySelectorAll('a[href*="profile/uid"]').forEach(a => {
                    const m = (a.href || '').match(/profile\\/uid\\/(\\w+)\\/(\\d+)/);
                    if (!m) return;
                    const pn = a.querySelector('.player-name');
                    const name = pn ? pn.textContent.trim() : a.textContent.trim().split(/Lvl|Prestige|Currently/)[0].trim();
                    const row = a.textContent;
                    const lv = (row.match(/Lvl\\s*(\\d+)/) || [])[1] || '';
                    const pr = (row.match(/Prestige\\s*(\\d+)/) || [])[1] || '';
                    const rp = (row.match(/([\\d,]+)\\s*RP/) || [])[1] || '';
                    const ri = a.querySelector('img[src*="ranks"]');
                    const rank_img = ri ? ri.src : '';
                    items.push({name, uid: m[2], platform: m[1], level: lv, prestige: pr, rp: rp.replace(/,/g,''), rank_img});
                });
                if (!items.length) {
                    const name = (document.querySelector('.player-name') || {}).textContent?.trim();
                    const uid = (document.getElementById('puid') || {}).value;
                    if (name && uid) items.push({name, uid, platform: '""" + platform + """'});
                }
                const seen = new Set();
                return items.filter(i => { const k = i.uid; if (seen.has(k)) return false; seen.add(k); return true; }).slice(0, 10);
            }""")
            return result
        except Exception as e:
            logger.error(f"[SearchPlayers] Error: {e}")
            return []
