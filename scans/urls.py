from django.urls import path

from .views import (
    connection_failed_hx,
    connection_test,
    scan_home_page,
    scan_hx,
    send_failed_hx,
)

app_name = "scans"

urlpatterns = [
    path("", view=scan_home_page, name="scan"),
    path("scan_hx", view=scan_hx, name="scan_hx"),
    path("resend_scans_hx", view=send_failed_hx, name="resend_scans_hx"),
    path("internet-poll", view=connection_test, name="internet_poll"),
    path("button-poll", view=connection_failed_hx, name="hx_button_poll"),
]
