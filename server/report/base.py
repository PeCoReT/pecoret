import matplotlib.font_manager as font_manager
import matplotlib as mpl
from backend.models import Finding
from . import config


class FontMixin:
    def initialize_fonts(self, base_dir):
        font_manager.fontManager.addfont(str(base_dir / 'templates/fonts/roboto/Roboto-Regular.ttf'))
        font_manager.fontManager.addfont(str(base_dir / 'templates/fonts/roboto/Roboto-Bold.ttf'))
        font_manager.fontManager.addfont(str(base_dir / 'templates/fonts/roboto/Roboto-Light.ttf'))
        mpl.rcParams['font.family'] = 'Roboto'
        mpl.rcParams['font.size'] = 9


class DefaultBaseTemplate(FontMixin):
    """
    some common setups and adjustments across finding exports, pdf reports, ...
    """
    config = config

    def check_finding_errors(self):
        for finding in Finding.objects.for_report(self.get_project()):
            if not finding.proof_text:
                self.add_report_error("Missing proof!", f"#finding-{finding.pk}-proofs")
            if self.get_project().require_cvss_base_score and finding.cvssbasescore.is_incomplete:
                self.add_report_error("Missing CVSS base score", f"#finding-{finding.pk}-title")
