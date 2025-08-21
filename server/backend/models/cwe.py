from django.db import models


class EntryType(models.IntegerChoices):
    WEAKNESS = 0, "Weakness"
    CATEGORY = 1, "Category"


class CWE(models.Model):
    cwe_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=512)
    description = models.TextField()
    extended_description = models.TextField(blank=True)
    entry_type = models.SmallIntegerField(choices=EntryType.choices)

    class Meta:
        ordering = ["cwe_id"]
        verbose_name = "CWE"
        verbose_name_plural = "CWEs"

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return f"CWE-{self.cwe_id}"

    @property
    def url(self):
        return f"https://cwe.mitre.org/data/definitions/{self.cwe_id}.html"
