from pecoret.reporting.template.errors.base import BaseErrorCheck


class VersionHistoryCheck(BaseErrorCheck):

    def check(self, context, **kwargs):
        errors = []
        report_doc = context.get('report_document')
        if not report_doc:
            return
        report = report_doc.report
        if not report.changehistory_set.count():
            url = '#change-history-table'
            errors.append(
                self.create_error('Missing version history', url)
            )
        return errors
