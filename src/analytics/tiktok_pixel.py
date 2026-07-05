"""TikTok Pixel integration for Streamlit (PageView + custom events)."""

from __future__ import annotations

import json
import os
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

# ── Configuration ─────────────────────────────────────────────────────────────
# Paste your Pixel ID here OR set TIKTOK_PIXEL_ID in .env (recommended for deploy)
TIKTOK_PIXEL_ID = "D958TUBC77U79CKEPSA0"

_PLACEHOLDER_IDS = {"", "PASTE_MY_PIXEL_ID_HERE", "YOUR_PIXEL_ID", "YOUR_PIXEL_ID_HERE"}

_PRODUCT_ID = "alphabtc-trading-tool"
_PRODUCT_NAME = "Alpha BTC Trading Tool"
_PRODUCT_VALUE = 99.0
_PRODUCT_CURRENCY = "USD"

_QUEUE_KEY = "_tiktok_event_queue"


def get_pixel_id() -> str:
    """Return the configured Pixel ID (.env overrides the constant when non-placeholder)."""
    env_val = os.getenv("TIKTOK_PIXEL_ID", "").strip()
    if env_val and env_val not in _PLACEHOLDER_IDS:
        return env_val
    if TIKTOK_PIXEL_ID not in _PLACEHOLDER_IDS:
        return TIKTOK_PIXEL_ID
    return env_val or TIKTOK_PIXEL_ID


def is_pixel_enabled() -> bool:
    """True when a real Pixel ID is configured."""
    return get_pixel_id() not in _PLACEHOLDER_IDS


def _default_product_props(**extra: Any) -> dict[str, Any]:
    props: dict[str, Any] = {
        "content_id": _PRODUCT_ID,
        "content_name": _PRODUCT_NAME,
        "content_type": "product",
        "value": _PRODUCT_VALUE,
        "currency": _PRODUCT_CURRENCY,
    }
    props.update(extra)
    return props


def _queue_event(event: str, properties: dict[str, Any] | None = None) -> None:
    """Queue an event to fire on the next pixel render (same Streamlit rerun)."""
    if not is_pixel_enabled():
        return
    queue: list[dict[str, Any]] = st.session_state.setdefault(_QUEUE_KEY, [])
    queue.append({"event": event, "properties": properties or {}})


def _drain_queued_events() -> list[dict[str, Any]]:
    events = st.session_state.pop(_QUEUE_KEY, [])
    return events if isinstance(events, list) else []


def track_view_content(**properties: Any) -> None:
    """Queue TikTok ViewContent — product/page viewed."""
    _queue_event("ViewContent", _default_product_props(**properties))


def track_initiate_checkout(**properties: Any) -> None:
    """Queue TikTok InitiateCheckout — user started purchase flow."""
    _queue_event("InitiateCheckout", _default_product_props(**properties))


def track_complete_payment(**properties: Any) -> None:
    """Queue TikTok CompletePayment — payment or access success."""
    _queue_event("CompletePayment", _default_product_props(**properties))


def handle_payment_success_query() -> None:
    """
    Fire CompletePayment when the success URL is loaded.

    Example return URL after payment:
      https://alphabtctrading.com/?payment=success
    """
    if not is_pixel_enabled():
        return
    params = st.query_params
    payment_flag = str(params.get("payment", "")).lower()
    checkout_flag = str(params.get("checkout", "")).lower()
    if payment_flag in {"success", "complete", "1", "true"} or checkout_flag in {
        "success",
        "complete",
        "paid",
    }:
        if not st.session_state.get("_tiktok_complete_payment_fired"):
            track_complete_payment()
            st.session_state["_tiktok_complete_payment_fired"] = True


def inject_tiktok_pixel(
    *,
    page_view: bool = True,
    attach_purchase_listeners: bool = False,
) -> None:
    """
    Load the official TikTok Pixel on every Streamlit rerun.

    - PageView: ttq.page() on each load (requirement #4)
    - Queued events: ViewContent / InitiateCheckout / CompletePayment helpers
    - Optional JS listeners for Buy / Purchase / Get Access clicks (requirement #6)
    """
    if not is_pixel_enabled():
        return

    pixel_id = get_pixel_id()
    queued_events = _drain_queued_events()
    events_json = json.dumps(queued_events)
    attach_js = "true" if attach_purchase_listeners else "false"

    # streamlit.components.v1.html — official TikTok base pixel + ttq.page() PageView
    components.html(
        f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<script>
(function () {{
  var PIXEL_ID = {json.dumps(pixel_id)};
  var QUEUED = {events_json};
  var ATTACH_PURCHASE = {attach_js};
  var PRODUCT = {json.dumps(_default_product_props())};

  !function (w, d, t) {{
    w.TiktokAnalyticsObject = t;
    var ttq = w[t] = w[t] || [];
    ttq.methods = [
      "page","track","identify","instances","debug","on","off","once","ready",
      "alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"
    ];
    ttq.setAndDefer = function (obj, method) {{
      obj[method] = function () {{
        obj.push([method].concat(Array.prototype.slice.call(arguments, 0)));
      }};
    }};
    for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
    ttq.instance = function (id) {{
      var inst = ttq._i[id] || [];
      for (var j = 0; j < ttq.methods.length; j++) ttq.setAndDefer(inst, ttq.methods[j]);
      return inst;
    }};
    ttq.load = function (id, opts) {{
      var src = "https://analytics.tiktok.com/i18n/pixel/events.js";
      ttq._i = ttq._i || {{}};
      ttq._i[id] = [];
      ttq._i[id]._u = src;
      ttq._t = ttq._t || {{}};
      ttq._t[id] = +new Date();
      ttq._o = ttq._o || {{}};
      ttq._o[id] = opts || {{}};
      var s = document.createElement("script");
      s.type = "text/javascript";
      s.async = true;
      s.src = src + "?sdkid=" + id + "&lib=" + t;
      var first = document.getElementsByTagName("script")[0];
      first.parentNode.insertBefore(s, first);
    }};
  }}(window, document, "ttq");

  ttq.load(PIXEL_ID);

  /* TikTok event #1 — PageView on every Streamlit page load */
  {"ttq.page();" if page_view else "// PageView disabled for this render"}

  /* TikTok events #2–#4 — queued helper events (ViewContent / InitiateCheckout / CompletePayment) */
  QUEUED.forEach(function (item) {{
    ttq.track(item.event, item.properties || {{}});
  }});

  function fireInitiateCheckout() {{
    /* TikTok event — InitiateCheckout (purchase intent) */
    ttq.track("InitiateCheckout", PRODUCT);
  }}

  function fireCompletePayment() {{
    /* TikTok event — CompletePayment (successful payment / access) */
    ttq.track("CompletePayment", PRODUCT);
  }}

  function attachCheckoutListeners() {{
    if (!ATTACH_PURCHASE) return;
    try {{
      var doc = window.parent.document;

      /* Explicit hooks in login purchase panel HTML */
      doc.querySelectorAll("[data-tiktok-initiate-checkout]").forEach(function (el) {{
        if (el.dataset.tiktokBound === "1") return;
        el.dataset.tiktokBound = "1";
        el.addEventListener("click", fireInitiateCheckout);
      }});

      /* Match Buy / Purchase / Get Access buttons anywhere in the app */
      var labels = ["buy", "purchase", "get access"];
      doc.querySelectorAll("button, a[role='button'], [data-testid='stFormSubmitButton'] button").forEach(function (el) {{
        var text = (el.innerText || el.textContent || "").toLowerCase().trim();
        if (!labels.some(function (label) {{ return text.indexOf(label) !== -1; }})) return;
        if (el.dataset.tiktokBound === "1") return;
        el.dataset.tiktokBound = "1";
        el.addEventListener("click", fireInitiateCheckout);
      }});
    }} catch (err) {{
      /* Parent DOM may not be ready yet — retried below */
    }}
  }}

  attachCheckoutListeners();
  setTimeout(attachCheckoutListeners, 600);
  setTimeout(attachCheckoutListeners, 1500);

  window.__alphabtcTikTok = {{
    trackViewContent: function () {{ ttq.track("ViewContent", PRODUCT); }},
    trackInitiateCheckout: fireInitiateCheckout,
    trackCompletePayment: fireCompletePayment
  }};
}})();
</script>
</body>
</html>
        """,
        height=0,
        width=0,
        scrolling=False,
    )
