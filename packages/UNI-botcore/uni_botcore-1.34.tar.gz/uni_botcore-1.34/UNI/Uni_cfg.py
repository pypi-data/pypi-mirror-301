import asyncio
import aiohttp
from argparse import Namespace
import traceback
import json
from decimal import Decimal
import inspect
import time
from typing import List, Optional
import types
from os.path import basename, splitext
import functools
from functools import wraps
import textwrap
from random import randint
import httpx
from urllib.parse import urlparse
from typing import Optional, Callable, Dict, Any, List, Set
import paramiko
import os
import urllib.request as urllib_request
import importlib.util as importlib_util
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib

# from methods import texts, keyboards

# from Data_ import Packs as Custom_Packs

UNI_Handlers = {}
pre_UNI_Handlers = {}

Bot_Object = None

texts, keyboards = None, None
Custom_Packs = None

v_ = '1.34'