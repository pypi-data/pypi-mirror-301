# Copyright (c) 2024 iiPython

# Modules
from datetime import datetime, timedelta

from requests import Session

from usps.utils import LOCAL_TIMEZONE
from . import USER_AGENT, Package, Step
from .exceptions import StatusNotAvailable

# Main class
class UPSTracking:
    _session: Session | None = None

    @classmethod
    def track_package(cls, tracking_number: str) -> Package:
        if cls._session is None:
            cls._session = Session()

        if not cls._session.cookies:
            cls._session.get("https://www.ups.com/track", headers = {"User-Agent": USER_AGENT})

        response = cls._session.post(
            "https://webapis.ups.com/track/api/Track/GetStatus?loc=en_US",
            json = {"Locale": "en_US", "TrackingNumber": [tracking_number]},
            headers = {
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": USER_AGENT,
                "X-XSRF-TOKEN": cls._session.cookies["X-XSRF-TOKEN-ST"]
            }
        ).json()
        if response["statusCode"] != "200":
            raise StatusNotAvailable(response["statusText"])

        data = response["trackDetails"][0]

        # Bundle together
        return Package(
            None,
            data["shipmentProgressActivities"][0]["activityScan"],
            [x for x in data["milestones"] if x["isCurrent"]][-1]["name"],
            [
                Step(
                    step["milestoneName"]["name"],
                    step["location"],
                    datetime.strptime(f"{step['gmtDate']} {step['gmtTime']}", "%Y%m%d %H:%M:%S").replace(tzinfo = LOCAL_TIMEZONE) +\
                         timedelta(hours = int(step["gmtOffset"].split(":")[0]))
                )
                for step in data["shipmentProgressActivities"]
            ]
        )
