import json

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from requests.structures import CaseInsensitiveDict

from .helpers import is_connected, process_sortly
from .models import Scan


def connection_test(request):

    return render(
        request, "partials/internet.html", {"is_connected": is_connected("google.com")}
    )


def button_test_hx(request):
    scans = Scan.objects.all().order_by("-time_scan")[:100]  # Limit for performance

    has_non_uploaded = False

    for scan in scans:
        if scan.time_upload is None and scan.sku != "SCAN FAILED":
            has_non_uploaded = True
            break

    return render(
        request,
        "partials/resend_failed_button.html",
        {
            "scans": scans,
            "is_connected": is_connected("google.com"),
            "scan_button_on": True
            if (has_non_uploaded is True and is_connected("google.com"))
            else False,
        },
    )


def scan_home_page(request):

    scans = Scan.objects.all().order_by("-time_scan")[:100]  # Limit for performance
    
    # Get scan mode from session, default to IN
    scan_mode = request.session.get("scan_mode", "IN")

    return render(
        request,
        "scan.html",
        {
            "scans": scans,
            "is_connected": False,
            "scan_button_on": False,
            "location_name": settings.LOCATION_NAME,
            "location_code": settings.LOCATION_CODE,
            "scan_mode": scan_mode,
        },
    )


def toggle_scan_mode_hx(request):
    """Toggle scan mode between IN and OUT - called via AJAX"""
    current_mode = request.session.get("scan_mode", "IN")
    new_mode = "OUT" if current_mode == "IN" else "IN"
    request.session["scan_mode"] = new_mode
    request.session.modified = True
    request.session.save()  # Explicitly save session
    
    # Return JSON response for AJAX call
    from django.http import JsonResponse
    return JsonResponse({"status": "success", "mode": new_mode})


def scan_hx(request):

    scanner_input = request.POST.get("sku")

    if scanner_input != "" and scanner_input[0] != " " and "sy://" not in scanner_input:

        try:
            scan_dict = json.loads(scanner_input)
        except json.decoder.JSONDecodeError:
            scan_dict = {"tracking": ""}

    elif "sy://" in scanner_input:
        scan_dict = process_sortly(scanner_input)

    else:
        scan_dict = {"tracking": ""}

    # Get scan mode from session, default to IN (READ ONLY - don't modify session)
    scan_mode = request.session.get("scan_mode", "IN")
    
    # Calculate location code based on mode
    location_code = settings.LOCATION_CODE
    if scan_mode == "OUT":
        location_code = settings.LOCATION_CODE + 10

    if scan_dict["tracking"] != "":

        Scan.objects.create(
            sku=scan_dict["item"],
            tracking=scan_dict["tracking"],
            location=location_code,
        )

    else:

        Scan.objects.create(sku="SCAN FAILED", location=location_code)

    return render(
        request,
        "partials/hx_table.html",
        {
            "scans": Scan.objects.all().order_by("-time_scan")[:100],  # Limit for performance
            "scan_button_on": False,
        },
    )


def send_scans_hx(request):
    internet_status = 0
    payload = {"data": []}

    Scan.objects.filter(sku="").update(sku="NONE")

    for scan in (
        Scan.objects.filter(time_upload=None).exclude(sku="SCAN FAILED").exclude(sku="")
    ):

        payload["data"].append(
            {
                "type": "scans",
                "id": str(scan.scan_id),
                "attributes": {
                    "sku": scan.sku,
                    "location": scan.location,
                    "tracking": scan.tracking,
                    "time_scan": scan.time_scan.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                },
            }
        )
    if is_connected("google.com"):

        try:

            app_key = settings.APP_KEY

            data_json = json.dumps(payload)

            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Content-type"] = "application/json"
            headers["Authorization"] = "Token {}".format(app_key)

            response = requests.post(
                settings.SCANS_API_ENDPOINT, data=data_json, headers=headers
            )
            print(response.json())
            if response.status_code == 200:
                for obj in response.json()["data"]:

                    return_scan = Scan.objects.get(scan_id=obj["id"])
                    return_scan.time_upload = obj["attributes"]["time_upload"]
                    return_scan.save()
                    print(return_scan.scan_id)

            if response.status_code == 403:
                print("API KEY ERROR")

            internet_status = 1

        except KeyError:
            pass

    return render(
        request,
        "partials/hx_table.html",
        {
            "scans": Scan.objects.all().order_by("-time_scan")[:100],  # Limit for performance
            "internet_status": internet_status,
        },
    )


def delete_scan_hx(request, pk):

    try:
        Scan.objects.get(id=pk).delete()

    except Scan.DoesNotExist:
        pass

    return HttpResponse("")


def clear_bad_scans(request):

    Scan.objects.filter(time_upload=None).delete()
    Scan.objects.filter(tracking=None).delete()

    return HttpResponse("Done")
