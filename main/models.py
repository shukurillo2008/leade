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

    def save(self, *args, **kwargs):
        if self.company_uuid == False:
            statuses = Status.objects.filter(board=self)
            for status in statuses:
                status.is_active = False
                status.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ["-created_at"]


class Status(BaseModel):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.board == False:
            leadtypes = LeadType.objects.filter(status=self)
            for leadtype in leadtypes:
                leadtype.is_active = False
                leadtype.save()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
        ordering = ["order", "-created_at"]


class LeadType(BaseModel):
    name = models.CharField(max_length=100)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="leadtypes")
    description = models.TextField(default="null")
    order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.status == False:
            leads = Lead.objects.filter(type=self)
            for lead in leads:
                lead.is_active = False
                lead.save()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Lead Type"
        verbose_name_plural = "Lead Types"
        ordering = ["order", "-created_at"]

class Lead(BaseModel):
    title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        choices=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        max_length=100,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=300, default="null")
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


















