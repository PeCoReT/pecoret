<script>
export default {
    name: 'TargetDetailTabMenu',
    data() {
        return {
            items: [
                {
                    label: 'Details',
                    route: this.$router.resolve({
                        name: 'ASMonitorTargetDetail',
                        params: {
                            programId: this.$route.params.programId,
                            targetId: this.$route.params.targetId
                        }
                    })
                },
                {
                    label: 'Hostnames',
                    route: this.$router.resolve({
                        name: 'ASMonitorHostnameList',
                        params: {
                            programId: this.$route.params.programId,
                            targetId: this.$route.params.targetId
                        }
                    })
                },
                {
                    label: 'Ports',
                    route: this.$router.resolve({
                        name: 'ASMonitorPortList',
                        params: {
                            programId: this.$route.params.programId,
                            targetId: this.$route.params.targetId
                        }
                    })
                },
                {
                    label: 'URLs',
                    route: this.$router.resolve({
                        name: 'ASMonitorURLList',
                        params: {
                            programId: this.$route.params.programId,
                            targetId: this.$route.params.targetId
                        }
                    })
                },
                {
                    label: 'Findings',
                    route: this.$router.resolve({
                        name: 'ASMonitorTargetDetail',
                        params: {
                            programId: this.$route.params.programId,
                            targetId: this.$route.params.targetId
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
