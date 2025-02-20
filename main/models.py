from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    

    class Meta:
        abstract = True


class Board(BaseModel):
    company_uuid = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ["-created_at"]


class Status(BaseModel):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
        ordering = ["order", "-created_at"]


class LeadType(BaseModel):
    name = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Lead Type"
        verbose_name_plural = "Lead Types"
        ordering = ["order", "-created_at"]

class Lead(BaseModel):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    type = models.ForeignKey(LeadType, on_delete=models.CASCADE)
    extra = models.JSONField(default=dict, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["order", "-created_at"]

class LeadHistory(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    lead_type = models.ForeignKey(LeadType, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lead History"
        verbose_name_plural = "Lead Histories"
        ordering = ["-created_at"]


















