<script>
import { useASMonitorStore } from '@/store/asMonitor';
import ASMonitorService from '@/service/ASMonitorService';

export default {
    name: 'ProgramTabMenu',
    mounted() {
        if (!this.asMonitorStore.activeProgram.name) {
            this.service.getProgram(this.$api, this.$route.params.programId).then((response) => {
                this.asMonitorStore.activateProgram(response.data);
            });
        }
    },
    data() {
        return {
            asMonitorStore: useASMonitorStore(),
            service: new ASMonitorService(),
            items: [
                {
                    label: 'Overview',
                    route: this.$router.resolve({
                        name: 'ASMonitorProgramDetail',
                        params: {
                            programId: this.$route.params.programId
                        }
                    }).path
                },
                {
                    label: 'Targets',
                    route: this.$router.resolve({
                        name: 'ASMonitorTargetList',
                        params: {
                            programId: this.$route.params.programId
                        }
                    }).path
                },
                {
                    label: 'Findings',
                    route: this.$router.resolve({
                        name: 'ASMonitorFindingList',
                        params: {
                            programId: this.$route.params.programId
                        }
                    }).path
                },
                {
                    label: 'Scans'
                }
            ]
        };
    }
};
</script>
<template>
    <Menubar :model="items" class="surface-card">
        <template #item="{ label, item, props, root, hasSubmenu }">
            <router-link v-if="item.route" v-slot="routerProps" :to="item.route">
                <span v-bind="props.action">
                    <span v-bind="props.icon" />
                    <span v-bind="props.label">{{ label }}</span>
                </span>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
                <span v-bind="props.icon" />
                <span v-bind="props.label">{{ label }}</span>
                <span :class="[hasSubmenu && (root ? 'pi pi-fw pi-angle-down' : 'pi pi-fw pi-angle-right')]" v-bind="props.submenuicon" />
            </a>
        </template>
    </Menubar>
</template>
