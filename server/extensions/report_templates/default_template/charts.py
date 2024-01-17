import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager
from pathlib import Path
from matplotlib.ticker import MaxNLocator
from django.utils.translation import gettext as _
from pecoret.reporting.components.chart import Chart


class FindingBarChart(Chart):
    def __init__(self, findings, colors):
        super().__init__()
        self.findings = findings
        self.colors = colors
        origin = Path(__file__).parent
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Regular.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Bold.ttf'))
        font_manager.fontManager.addfont(str(origin / 'templates/fonts/roboto/Roboto-Light.ttf'))
        mpl.rcParams['font.family'] = 'Roboto'
        mpl.rcParams['font.size'] = 9

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
        colors = [
            self.colors['critical'], self.colors['high'], self.colors['medium'],
            self.colors['low'], self.colors['informational']
        ]
        ax.bar(labels, counts, color=colors)
        ya = ax.get_yaxis()
        ya.set_major_locator(MaxNLocator(integer=True))
        return self.to_html(plt)
