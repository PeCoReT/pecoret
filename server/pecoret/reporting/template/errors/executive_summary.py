from pecoret.reporting.template.errors.base import BaseErrorCheck


class ExecutiveSummaryCheck(BaseErrorCheck):

    def check(self, context, **kwargs):
        errors = []
        report_doc = context.get('report_document')
        if not report_doc:
            return
        report = report_doc.report
        if not report.recommendation:
            url = '#executive-summary-recommendation'
            errors.append(
                self.create_error('Missing recommendation in executive summary', url)
            )
        if not report.evaluation:
            url = '#executive-summary-evaluation'
            errors.append(
                self.create_error('Missing evaluation in executive summary', url)
            )
        return errors
