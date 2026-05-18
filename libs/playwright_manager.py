"""共享 Playwright 浏览器管理器 — 单一持久进程，全局复用"""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Browser

_playwright = None
_browser: Browser | None = None
_lock = asyncio.Lock()
_semaphore = asyncio.Semaphore(2)

# 性能监控
_stats: dict[str, list[float]] = {
    "sem_wait": [],   # 等待信号量的耗时
    "ctx_create": [],  # 创建上下文的耗时
    "page_use": [],    # 使用页面的总耗时
}


def _log_stat(key: str, value: float):
    _stats[key].append(value)
    # 保留最近20条
    if len(_stats[key]) > 20:
        _stats[key] = _stats[key][-20:]


def get_pw_stats() -> dict:
    """获取 Playwright 性能统计"""
    result = {}
    for k, v in _stats.items():
        if v:
            result[k] = {
                "avg": sum(v) / len(v),
                "max": max(v),
                "min": min(v),
                "count": len(v),
            }
    return result


async def get_browser() -> Browser:
    global _playwright, _browser
    if _browser is None:
        async with _lock:
            if _browser is None:
                _playwright = await async_playwright().start()
                _browser = await _playwright.webkit.launch(headless=True)
    return _browser


async def close_browser():
    global _playwright, _browser
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright:
        await _playwright.stop()
        _playwright = None


@asynccontextmanager
async def run_with_page(viewport: dict = None, device_scale_factor: float = 1):
    t_wait = time.perf_counter()
    async with _semaphore:
        _log_stat("sem_wait", time.perf_counter() - t_wait)

        t_ctx = time.perf_counter()
        browser = await get_browser()
        ctx = await browser.new_context(
            viewport=viewport,
            device_scale_factor=device_scale_factor,
        )
        page = await ctx.new_page()
        _log_stat("ctx_create", time.perf_counter() - t_ctx)

        t_use = time.perf_counter()
        try:
            yield page
        finally:
            _log_stat("page_use", time.perf_counter() - t_use)
            await ctx.close()
