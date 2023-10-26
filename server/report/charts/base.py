import io
import matplotlib as mpl
from django.utils.html import format_html


class BaseChart:
    def __init__(self, *args, **kwargs):
        mpl.use('Agg')

    def plot(self):
        raise NotImplementedError()

    def to_html(self, plot, css_class="chart"):
        f = io.StringIO()
        plot.savefig(f, format='svg', transparent=True)
        plot.close('all')
        return format_html('<img class="{}" src="data:image/svg+xml;utf8,{}">', css_class, f.getvalue())
