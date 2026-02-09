#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临时调试脚本 - 避免会话退出时报错
"""

import sys

try:
    input_data = sys.stdin.read() if hasattr(sys.stdin, 'read') else ""
    print(input_data if input_data else "", flush=True)
except:
    pass
