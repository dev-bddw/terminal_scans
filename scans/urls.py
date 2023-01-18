from django.urls import path

from .views import (
    button_test_hx,
    connection_test,
    scan_home_page,
    scan_hx,
    send_scans_hx,
    delete_scan_hx,
    clear_bad_scans,
)

app_name = "scans"

urlpatterns = [
    path("", view=scan_home_page, name="scan"),
    path("scan_hx", view=scan_hx, name="scan_hx"),
    path("resend_scans_hx", view=send_scans_hx, name="resend_scans_hx"),
    path("internet-poll", view=connection_test, name="internet_poll"),
    path("button-poll", view=button_test_hx, name="hx_button_poll"),
    path("clear/", clear_bad_scans, name="clear_bad_scans"),
    path("delete-scan/<pk>", view=delete_scan_hx, name="delete_scan_hx"),
]
