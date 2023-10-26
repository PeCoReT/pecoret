import matplotlib.pyplot as plt
from django.utils.translation import gettext as _
from matplotlib.ticker import MaxNLocator
from .base import BaseChart


class FindingBarChart(BaseChart):
    def __init__(self, findings, config):
        super().__init__()
        self.findings = findings
        self.config = config

    def plot(self):
        fig, ax = plt.subplots(figsize=[6, 2.5])
        findings = self.findings.exclude_fixed()
        labels = [_('Critical'), _('High'), _('Medium'), _('Low'), _('Informational')]
        counts = [
            findings.with_severity('critical').count(),
            findings.with_severity('high').count(),
            findings.with_severity('medium').count(),
            findings.with_severity('low').count(),
            findings.with_severity('informational').count()
        ]
        colors = [self.config.CRITICAL, self.config.HIGH, self.config.MEDIUM,
                  self.config.LOW, self.config.INFORMATIONAL]
        ax.bar(labels, counts, color=colors)
        ya = ax.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        return self.to_html(plt)
