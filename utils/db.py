"""
utils/db.py — Supabase database wrapper
All table operations centralised here. Swap backend by replacing this file only.
"""

from __future__ import annotations
import streamlit as st
from supabase import create_client, Client
from typing import Any


@st.cache_resource
def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def _invalidate_cache():
    """Call after any write operation to bust stale reads."""
    get_all_records.clear()


@st.cache_data(ttl=60)
def get_all_records(table: str, order_col: str = "created_at") -> list[dict]:
    """Fetch all rows from a table, newest first."""
    client = get_client()
    res = client.table(table).select("*").order(order_col, desc=True).execute()
    return res.data or []


def insert_record(table: str, data: dict) -> dict:
    client = get_client()
    res = client.table(table).insert(data).execute()
    _invalidate_cache()
    return res.data[0] if res.data else {}


def update_record(table: str, record_id: Any, data: dict, id_col: str = "id") -> dict:
    client = get_client()
    res = client.table(table).update(data).eq(id_col, record_id).execute()
    _invalidate_cache()
    return res.data[0] if res.data else {}


def delete_record(table: str, record_id: Any, id_col: str = "id") -> bool:
    client = get_client()
    client.table(table).delete().eq(id_col, record_id).execute()
    _invalidate_cache()
    return True


def query(table: str, filters: dict | None = None) -> list[dict]:
    """Filtered query — filters = {column: value}."""
    client = get_client()
    q = client.table(table).select("*")
    if filters:
        for col, val in filters.items():
            q = q.eq(col, val)
    return q.execute().data or []
