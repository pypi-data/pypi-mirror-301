from __future__ import annotations

import json
import os
import tempfile
import time
from pathlib import Path
from typing import Any

import requests
from tenacity import RetryError, Retrying, stop_after_delay, wait_random_exponential

from piiip._logger import logger

PYPISTATS_HTTP_CODE_RATE_LIMITING = 429

CACHE_LIFETIME = (
    60 * 60 * 24
)  # pypistats.org updates its data once a day: https://pypistats.org/api/


class Cache:
    CACHE_DIR: Path
    CACHE_FILE: Path
    saved_data: dict[str, tuple[float, Any]]

    def __new__(cls) -> Cache:
        """
        Singleton
        """
        if not hasattr(cls, "_instance"):
            instance = super().__new__(cls)
            instance.CACHE_DIR = _get_cache_dir()
            instance.CACHE_FILE = instance.CACHE_DIR / "piiip.cache"
            logger.debug(f"cache directory: {instance.CACHE_DIR!s}")

            if not instance.CACHE_FILE.exists():
                instance.CACHE_FILE.write_text(json.dumps({}))
            with instance.CACHE_FILE.open() as file:
                instance.saved_data = json.loads(file.read())
            cls._instance = instance

        return cls._instance

    def get_json(self, url: str) -> Any:
        """
        Gets a JSON object from either the cache or the provided URL.
        If the URL returns status code 404, an empty dictionary is returned.
        """
        # Try to get the data from the cache
        if url in self.saved_data:
            timestamp, data = self.saved_data[url]
            if time.time() - timestamp < CACHE_LIFETIME:
                return data

        # Get the data from online
        r = self._get_with_rate_limit_retry(url)
        if r.status_code != 200:
            if r.status_code == 404:
                self.saved_data[url] = (time.time(), {})
                return {}
            else:
                raise RuntimeError(
                    f"Request for download of {url} resulted in {r.status_code}{r}"
                )
        else:
            self.saved_data[url] = (time.time(), r.json())
        return r.json()

    def _get_with_rate_limit_retry(self, url: str) -> requests.Response:
        try:
            for _ in Retrying(
                stop=stop_after_delay(10),
                wait=wait_random_exponential(min=0.2, multiplier=4),
            ):
                r = requests.get(url)
                if r.status_code != PYPISTATS_HTTP_CODE_RATE_LIMITING:
                    break
                logger.debug("Hit pypistats.org rate limiter")
        except RetryError:
            pass
        return r

    def get_file(self, protocol: str, FQDN: str, file: str) -> Path:
        """
        protocol: the protocol (e.g. "https" or "http")
        FQDN: the fully qualified domain name (e.g. "pypi.org")
        file: the path and name of the file that should be downloaded (e.g. "simple" or "project/pandas/")
        """
        # Try to get the file from the cache
        cache_file = self.CACHE_DIR / f"{file}.cache"
        if cache_file.is_file() and (
            time.time() - os.path.getmtime(cache_file) < CACHE_LIFETIME
        ):
            return cache_file

        logger.info("piiip: downloading up to date package index")
        # Get the file from online
        r = requests.get(f"{protocol}://{FQDN}/{file}")
        if r.status_code != 200:
            raise RuntimeError(f"Request for download resulted in {r.status_code}{r}")
        cache_file.write_text(r.text)
        return cache_file

    def save_cache_to_disk(self) -> None:
        # Collect all recent entries from the cache
        up_to_date_cache = {}
        if self.saved_data:
            for url, endpoint in self.saved_data.items():
                timestamp, data = endpoint
                if time.time() - timestamp < CACHE_LIFETIME:
                    up_to_date_cache[url] = (timestamp, data)

        # Write the recent entries to disk
        with open(self.CACHE_FILE, "w") as file:
            json.dump(up_to_date_cache, file)


def _get_cache_dir() -> Path:
    CACHE_DIR = Path(tempfile.gettempdir()).joinpath("piiip")
    CACHE_DIR.mkdir(exist_ok=True)
    return CACHE_DIR
