<script>
export default {
    name: 'AttackSurfaceTabMenu',
    data() {
        return {
            items: [
                {
                    label: 'Search',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceSearch'
                    })
                },
                {
                    label: 'Findings',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceFindingList'
                    })
                },
                {
                    label: 'Services',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceServiceList'
                    })
                },
                {
                    label: 'Targets',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceTargetList'
                    })
                },
                {
                    label: 'URLs',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceURLList'
                    })
                },
                {
                    label: 'Scan Findings',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScanFindingList'
                    })
                },
                {
                    label: 'Programs',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceProgramList'
                    })
                },
                {
                    label: 'Tags',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceTagList'
                    })
                },
                {
                    label: 'Scanning',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScanList'
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
