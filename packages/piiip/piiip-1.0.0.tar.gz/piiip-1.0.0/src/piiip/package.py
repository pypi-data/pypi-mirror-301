from __future__ import annotations

from piiip.cache import Cache


class Package:

    def __init__(self, package_name: str) -> None:
        self.name: str = package_name
        self.popularity: int = self.determine_popularity()

    def determine_popularity(self) -> int:
        """
        Determines how popular a package is. This is now determined
        solemnly on the download count.
        """
        response = Cache().get_json(
            f"https://pypistats.org/api/packages/{self.name}/recent"
        )
        if "data" in response:
            return int(response["data"]["last_month"])
        else:
            return 0  # the request resulted in a 404. Not all packages are listed on pypistats.org
