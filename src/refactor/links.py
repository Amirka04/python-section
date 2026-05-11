import datetime
from datetime import date
from typing import NamedTuple
import logging
from urllib.parse import urlparse

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BulletinLink(NamedTuple):
    """Ссылка на бюллетень с извлечённой датой."""
    url: str
    bulletin_date: date


def parse_page_links(html: str, start_date: date, end_date: date, base_url: str = "https://spimex.com") -> list[BulletinLink]:
    """
    Извлекает ссылки на бюллетени из HTML-страницы и фильтрует по диапазону дат.

    Args:
        html: HTML-содержимое страницы.
        start_date: Начало диапазона (включительно).
        end_date: Конец диапазона (включительно).
        base_url: Базовый URL для относительных ссылок.

    Returns:
        Список BulletinLink, отсортированных по дате (от старых к новым).
    """
    raw_links = _extract_raw_links(html)
    bulletins = _parse_bulletins(raw_links, base_url)
    filtered = _filter_by_date(bulletins, start_date, end_date)
    return sorted(filtered, key=lambda b: b.bulletin_date)


def _extract_raw_links(html: str) -> list[str]:
    """Извлекает href из подходящих тегов <a>."""
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")
    return [
        link.get("href", "")
        for link in links
        if link.get("href")
    ]


def _is_valid_bulletin_path(href: str) -> bool:
    """Проверяет, что ссылка ведёт на xls-бюллетень."""
    return "/upload/reports/oil_xls/oil_xls_" in href and href.endswith(".xls")


def _extract_date_from_href(href: str) -> date | None:
    """
    Пытается извлечь дату из ссылки в формате YYYYMMDD.

    Ожидаемый паттерн: .../oil_xls_20240101.xls
    """
    try:
        date_str = href.split("oil_xls_")[1][:8]
        return datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except (IndexError, ValueError):
        logger.debug("Не удалось извлечь дату из ссылки: %s", href)
        return None


def _make_absolute_url(href: str, base_url: str) -> str:
    """Приводит относительную ссылку к абсолютной, если нужно."""
    if href.startswith(("http://", "https://")):
        return href
    # Убираем query-параметры (редкий случай, но защита от дублирования)
    parsed = urlparse(href)
    clean_path = parsed.path
    return f"{base_url.rstrip('/')}/{clean_path.lstrip('/')}"


def _parse_bulletins(raw_links: list[str], base_url: str) -> list[BulletinLink]:
    """Преобразует сырые ссылки в BulletinLink, отбрасывая некорректные."""
    bulletins = []
    for href in raw_links:
        # Отсекаем query-параметры — бывают tracking-метки
        clean_href = href.split("?")[0]
        
        if not _is_valid_bulletin_path(clean_href):
            continue
        
        bulletin_date = _extract_date_from_href(clean_href)
        if bulletin_date is None:
            continue
        
        url = _make_absolute_url(clean_href, base_url)
        bulletins.append(BulletinLink(url=url, bulletin_date=bulletin_date))
    
    return bulletins


def _filter_by_date(
    bulletins: list[BulletinLink],
    start_date: date,
    end_date: date,
) -> list[BulletinLink]:
    """Фильтрует бюллетени по диапазону дат."""
    return [
        b for b in bulletins
        if start_date <= b.bulletin_date <= end_date
    ]