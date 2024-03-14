<script>
import ASMonitorService from '@/service/ASMonitorService';
import FindingCount from '@/components/asmonitor/programDashboard/FindingCount.vue';
import TargetCountCard from '@/components/asmonitor/programDashboard/TargetCountCard.vue';
import HighestSeverityCard from '@/components/asmonitor/programDashboard/HighestSeverityCard.vue';
import LatestTargetCard from '@/components/asmonitor/programDashboard/LatestTargetCard.vue';
import ProgramUpdateDialog from '@/components/asmonitor/ProgramUpdateDialog.vue';
import LatestFindings from "@/components/asmonitor/programDashboard/LatestFindings.vue";
import FindingsByDatesChart from "@/components/asmonitor/programDashboard/FindingsByDatesChart.vue";
import LatestTargets from "@/components/asmonitor/programDashboard/LatestTargets.vue";

export default {
    name: 'ProgramDetail.vue',
    components: {
        LatestTargets,
        FindingsByDatesChart,
        LatestFindings,
        ProgramUpdateDialog,
        LatestTargetCard,
        HighestSeverityCard,
        TargetCountCard,
        FindingCount,
    },
    data() {
        return {
            program: {},
            service: new ASMonitorService(),
            programId: this.$route.params.programId,
            breadcrumbs: [
                {
                    label: 'Programs',
                    to: this.$router.resolve({
                        name: 'ASMonitorProgramList'
                    })
                },
                {
                    label: 'Detail',
                    disabled: true
                }
            ]
        };
    },
    mounted() {
        this.getProgram();
    },
    methods: {
        getProgram() {
            this.service.getProgram(this.$api, this.programId).then((response) => {
                this.program = response.data;
            });
        }
    }
};
</script>

<template>
    <div class="grid mt-3">
        <div class="col-12">
            <pBreadcrumb v-model="breadcrumbs"></pBreadcrumb>
        </div>
    </div>
    <div class="grid">
        <div class="col-6"></div>
        <div class="col-6">
            <div class="flex justify-content-end">
                <ProgramUpdateDialog :program="program"></ProgramUpdateDialog>
            </div>
        </div>
    </div>
    <div class="grid">
        <div class="col-12 md:col-3">
            <FindingCount :program-id="program.pk"></FindingCount>
        </div>
        <div class="col-12 md:col-3">
            <TargetCountCard :program-id="program.pk"></TargetCountCard>
        </div>
        <div class="col-12 md:col-3">
            <HighestSeverityCard :program-id="program.pk"></HighestSeverityCard>
        </div>
        <div class="col-12 md:col-3">
            <LatestTargetCard :program-id="program.pk"></LatestTargetCard>
        </div>
    </div>
    <div class="grid">
        <div class="col-12 md:col-6">
            <LatestFindings :program-id="program.pk"></LatestFindings>
            <LatestTargets :program-id="program.pk"></LatestTargets>
        </div>
        <div class="col-12 md:col-6">
            <FindingsByDatesChart :program-id="program.pk"></FindingsByDatesChart>
        </div>
    </div>
</template>
