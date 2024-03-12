<script>
import ASMonitorService from '@/service/ASMonitorService';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import FindingCount from "@/components/asmonitor/programDashboard/FindingCount.vue";
import TargetCountCard from "@/components/asmonitor/programDashboard/TargetCountCard.vue";
import HighestSeverityCard from "@/components/asmonitor/programDashboard/HighestSeverityCard.vue";
import LatestTargetCard from "@/components/asmonitor/programDashboard/LatestTargetCard.vue";

export default {
    name: 'ProgramDetail.vue',
    components: { LatestTargetCard, HighestSeverityCard, TargetCountCard, FindingCount, MarkdownEditor },
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
        <div class="col-12">
            <div class="card">
                <div class="grid formgrid p-fluid">
                    <div class="field col-12">
                        <label for="name">Name</label>
                        <InputText id="name" v-model="program.name"></InputText>
                    </div>
                    <div class="field col-12">
                        <label for="description">Description</label>
                        <MarkdownEditor v-model="program.description"></MarkdownEditor>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
