import re
from datetime import datetime
from typing import List, Set, Optional, Iterable, Any
from xml.sax.saxutils import escape


class StringUtils:
    EMPTY_STRING_ARRAY = []
    TZ_GMT8 = "Asia/Shanghai"  # Assuming Constants.DATE_TIMEZONE is "Asia/Shanghai"
    PATTERN_CIDR = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})$")
    QUOT = "&quot;"
    AMP = "&amp;"
    APOS = "&apos;"
    GT = "&gt;"
    LT = "&lt;"

    @staticmethod
    def is_empty(value: Optional[str]) -> bool:
        if value is None or len(value.strip()) == 0:
            return True
        return False

    @staticmethod
    def is_numeric(obj: Any) -> bool:
        if obj is None:
            return False
        s = str(obj)
        if len(s) == 0:
            return False
        if s[0] == "-":
            s = s[1:]
        return s.isdigit()

    @staticmethod
    def are_not_empty(*values: Optional[str]) -> bool:
        if values is None or len(values) == 0:
            return False
        return all(not StringUtils.is_empty(value) for value in values)

    @staticmethod
    def unicode_to_chinese(unicode_str: str) -> str:
        return unicode_str if not StringUtils.is_empty(unicode_str) else ""

    @staticmethod
    def to_underline_style(name: str) -> str:
        return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip(
            "_"
        )

    @staticmethod
    def to_camel_style(name: str) -> str:
        return name[0].lower() + name[1:]

    @staticmethod
    def parse_date_time(date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise RuntimeError(e)

    @staticmethod
    def format_date_time(date: datetime) -> str:
        return date.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def format_date_time_with_pattern(date: datetime, pattern: str) -> str:
        return date.strftime(pattern)

    @staticmethod
    def escape_xml(value: str) -> str:
        return escape(
            value,
            {
                '"': StringUtils.QUOT,
                "&": StringUtils.AMP,
                "'": StringUtils.APOS,
                ">": StringUtils.GT,
                "<": StringUtils.LT,
            },
        )

    @staticmethod
    def get_class_properties(cls: Any, is_get: bool) -> Set[str]:
        prop_names = set()
        if cls is None:
            return prop_names
        for attr in dir(cls):
            if attr.startswith("_"):
                continue
            if is_get and callable(getattr(cls, attr)):
                prop_names.add(attr)
            elif not is_get and callable(getattr(cls, attr)):
                prop_names.add(attr)
        return prop_names

    @staticmethod
    def is_digits(s: Optional[str]) -> bool:
        return s.isdigit() if s else False

    @staticmethod
    def split(s: Optional[str], sep: Optional[str] = None) -> List[str]:
        if s is None:
            return []
        return s.split(sep) if sep else s.split()

    @staticmethod
    def is_ip_in_range(ip_addr: str, cidr_addr: str) -> bool:
        match = StringUtils.PATTERN_CIDR.match(cidr_addr)
        if not match:
            raise ValueError(f"Invalid CIDR address: {cidr_addr}")

        ip_parts = list(map(int, match.group(1).split(".")))
        int_mask = int(match.group(2))
        min_ip_parts = [0] * 4
        max_ip_parts = [0] * 4

        for i in range(4):
            if int_mask >= 8:
                min_ip_parts[i] = max_ip_parts[i] = ip_parts[i]
                int_mask -= 8
            elif int_mask > 0:
                mask = (0xFF >> int_mask) ^ 0xFF
                min_ip_parts[i] = ip_parts[i] & mask
                max_ip_parts[i] = ip_parts[i] | (0xFF >> int_mask)
                int_mask = 0
            else:
                min_ip_parts[i] = 0
                max_ip_parts[i] = 0xFF

        real_ip_parts = list(map(int, ip_addr.split(".")))
        return all(
            min_ip_parts[i] <= real_ip_parts[i] <= max_ip_parts[i] for i in range(4)
        )

    @staticmethod
    def join(objs: Iterable[Any], sep: str) -> str:
        return sep.join(map(str, objs))

    @staticmethod
    def join_appendable(
        buf: Any, objs: Iterable[Any], sep: Optional[str] = None
    ) -> None:
        sep = sep or ""
        buf.write(sep.join(map(str, objs)))
