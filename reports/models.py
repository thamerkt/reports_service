from django.db import models

class Rapport(models.Model):
    REPORT_TYPES = [
        ('financial', 'Financial Report'),
        ('rental', 'Rental Performance'),
        ('customer', 'Customer Feedback'),
        ('inventory', 'Inventory Report'),
        ('custom', 'Custom Report'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, default='custom')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(
        max_length=20,
        null=True, blank=True
    )
    user=models.CharField(max_length=255,null=True)

    def __str__(self):
        return f"{self.title} ({self.type}) - {self.date_created}"

class RapportData(models.Model):
    rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, related_name='data')  # One-to-Many
    metric_name = models.CharField(max_length=255)  # Example: "Total Revenue", "Items Rented"
    metric_value = models.FloatField()  # Example: 5000.00, 100
    unit = models.CharField(max_length=50, null=True, blank=True)  # Example: "$", "items", "days"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} {self.unit}"
