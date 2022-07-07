import json

import requests
from django.conf import settings
from django.shortcuts import render
from requests.structures import CaseInsensitiveDict

from .helpers import is_connected
from .models import Scan


def connection_test(request):

    internet_status = 1 if is_connected("google.com") else 0

    return render(
        request, "partials/internet.html", {"internet_status": internet_status}
    )


def connection_failed_hx(request):
    scans = Scan.objects.all().order_by("-time_scan")

    has_failed_scans = False

    for scan in scans:
        if scan.time_upload is None and scan.scan_id is None:
            has_failed_scans = True
            break
        else:
            has_failed_scans = False

    internet_status = 1 if is_connected("google.com") else 0

    return render(
        request,
        "partials/resend_failed_button.html",
        {
            "scans": scans,
            "internet_status": internet_status,
            "has_failed_scans": has_failed_scans,
        },
    )


def scan_home_page(request):

    scans = Scan.objects.all().order_by("-time_scan")

    has_failed_scans = False

    for scan in scans:
        if scan.time_upload is None and scan.scan_id is None:
            has_failed_scans = True
            break
        else:
            has_failed_scans = False

    internet_status = 1 if is_connected("google.com") else 0

    return render(
        request,
        "scan.html",
        {
            "scans": scans,
            "internet_status": internet_status,
            "has_failed_scans": has_failed_scans,
        },
    )


def scan_hx(request):

    sku = request.POST.get("sku")
    internet_status = 1

    scans = Scan.objects.all().order_by("-time_scan")

    has_failed_scans = [
        x for x in scans if (x.time_upload is None) and (x.scan_id is None)
    ]

    if sku != "":

        new_scan = Scan(sku=sku, location=settings.LOCATION_CODE)
        new_scan.save()

        if is_connected("google.com"):

            try:

                app_key = settings.APP_KEY
                scan_data = {
                    "sku": new_scan.sku,
                    "time_scan": new_scan.time_scan.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                    "location": new_scan.location,
                }

                data_json = json.dumps(scan_data)

                headers = CaseInsensitiveDict()
                headers["Accept"] = "application/json"
                headers["Content-type"] = "application/json"
                headers["Authorization"] = "Token {}".format(app_key)

                response = requests.post(
                    "https://bddwscans.com/endpoint/", data=data_json, headers=headers
                )

                if response.status_code == 200:
                    print(response.json())
                    new_scan.scan_id = response.json()["scan_id"]
                    new_scan.time_upload = response.json()["time_upload"]
                    new_scan.save()

                if response.status_code == 403:
                    print("API KEY ERROR")

            except requests.exceptions.ConnectionError:
                internet_status = 0
                print("There was a connection problem. Saving the scan locally.")
                pass
        else:
            internet_status = 0
            print("There was a connection problem")

        return render(
            request,
            "partials/hx_table.html",
            {
                "scans": Scan.objects.all().order_by("-time_scan"),
                "internet_status": internet_status,
                "has_failed_scans": has_failed_scans != [],
            },
        )

    else:
        return render(
            request,
            "partials/hx_table.html",
            {
                "scans": scans,
                "internet_status": internet_status,
                "has_failed_scans": has_failed_scans != [],
            },
        )


def send_failed_hx(request):

    internet_status = 1

    for scan in Scan.objects.filter(time_upload=None):
        if is_connected("google.com"):
            try:
                app_key = settings.APP_KEY
                scan_data = {
                    "sku": scan.sku,
                    "time_scan": scan.time_scan.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                    "location": scan.location,
                }
                data_json = json.dumps(scan_data)

                headers = CaseInsensitiveDict()
                headers["Accept"] = "application/json"
                headers["Content-type"] = "application/json"
                headers["Authorization"] = "Token {}".format(app_key)

                response = requests.post(
                    "https://bddwscans.com/endpoint/", data=data_json, headers=headers
                )

                if response.status_code == 200:
                    print(response.json())
                    scan.scan_id = response.json()["scan_id"]
                    scan.time_upload = response.json()["time_upload"]
                    scan.save()

                if response.status_code == 403:
                    print("API KEY ERROR")

            except requests.exceptions.ConnectionError:
                print("There was a connection problem. Saving the scan locally.")
                pass
        else:
            internet_status = 0
            print("There was a connection problem. Saving the scan locally.")

    return render(
        request,
        "partials/hx_table.html",
        {
            "scans": Scan.objects.all().order_by("-time_scan"),
            "internet_status": internet_status,
        },
    )
