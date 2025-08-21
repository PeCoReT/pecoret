<script>
import { Tabs } from '@/components/tabs';

export default {
    name: 'ReportTabMenu',
    components: { Tabs },
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
                    }).href
                },
                {
                    label: 'Version History',
                    route: this.$router.resolve({
                        name: 'ReportVersionHistoryList',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    }).href
                },
                {
                    label: 'Documents',
                    route: this.$router.resolve({
                        name: 'ReportDocumentList',
                        params: {
                            projectId: this.$route.params.projectId,
                            reportId: this.$route.params.reportId
                        }
                    }).href
                }
            ]
        };
    }
};
</script>

<template>
    <Tabs :item-length="3" :items="items"></Tabs>
</template>
