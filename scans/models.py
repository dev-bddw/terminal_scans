from django.db import models
import uuid

class Scan(models.Model):

    sku = models.CharField(blank=False, null=False, max_length=200)

    tracking = models.CharField(blank=True, null=True, max_length=200)

    time_scan = models.DateTimeField(auto_now_add=True)

    scan_id = models.UUIDField(default=uuid.uuid4, blank=True, null=True)

    location = models.IntegerField()

    time_upload = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-time_scan"]
