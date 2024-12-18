"""Utility functions for date handling"""
from datetime import datetime
from typing import Optional

def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Parse ISO format datetime string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None

def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime object to ISO format string"""
    if not dt:
        return None
    return dt.isoformat()