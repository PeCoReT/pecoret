<script>
import ASMonitorService from '@/service/ASMonitorService';
import BaseLayout from '@/layout/base/BaseLayout.vue';
import MarkdownEditor from '@/components/forms/MarkdownEditor.vue';
import TargetDetailTabMenu from '@/components/asmonitor/TargetDetailTabMenu.vue';

export default {
    name: 'TargetDetail',
    components: { TargetDetailTabMenu, MarkdownEditor, BaseLayout },
    data() {
        return {
            service: new ASMonitorService(),
            programId: this.$route.params.programId,
            targetId: this.$route.params.targetId,
            item: {},
            pagination: { limit: 25, page: 1 },
            totalRecords: 0,
            breadcrumbs: [
                {
                    label: 'Targets',
                    to: this.$router.resolve({
                        name: 'ASMonitorTargetList',
                        params: {
                            programId: this.$route.params.programId
                        }
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
        this.getItem();
    },
    methods: {
        getItem() {
            this.service.getTarget(this.$api, this.programId, this.targetId).then((resp) => {
                this.item = resp.data;
            });
        },
        patchItem(data) {
            this.service.patchTarget(this.$api, this.programId, this.targetId, data).then((resp) => {
                this.item = resp.data;
                this.$toast.add({
                    severity: 'success',
                    summary: 'Updated',
                    detail: 'Target updated!',
                    life: 3000
                });
            });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #default>
            <div class="col-12">
                <TargetDetailTabMenu class="surface-card"></TargetDetailTabMenu>
                <div class="card border-noround-top">
                    <div class="grid formgrid p-fluid">
                        <div class="field col-12">
                            <label for="description">Description</label>
                            <MarkdownEditor v-model="item.description" @blur="patchItem({ description: item.description })"></MarkdownEditor>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </BaseLayout>
</template>
