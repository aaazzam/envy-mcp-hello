"""Compatibility entry point for ``modal deploy devboxes.py::modal_app``."""

from envy_mcp_hello.app import app, hello, mcp, modal_app, serve

__all__ = ["app", "hello", "mcp", "modal_app", "serve"]
