<script>
export default {
    name: 'ReportTabMenu',
    data() {
        return {
            items: [
                {
                    label: 'Configuration',
                    route: this.$router.resolve({
                        name: 'ReportDetail',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Version History',
                    route: this.$router.resolve({
                        name: 'ReportVersionHistoryList',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                },
                {
                    label: 'Documents',
                    route: this.$router.resolve({
                        name: 'ReportDocumentList',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    })
                }
            ]
        };
    }
};
</script>

<template>
    <pTabMenu v-model="items"></pTabMenu>
</template>