<script>
import { Navbar } from '@/components/navbar';

export default {
    name: 'AttackSurfaceTabMenu',
    components: { Navbar },
    data() {
        return {
            items: [
                {
                    label: 'Search',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceSearch'
                    }),
                    icon: 'fa fa-search'
                },
                {
                    label: 'Findings',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceFindingList'
                    }),
                    icon: 'fa fa-bugs'
                },
                {
                    label: 'Targets',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceTargetList'
                    }),
                    icon: 'fa fa-crosshairs'
                },
                {
                    label: 'URLs',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceURLList'
                    }),
                    icon: 'fa fa-sitemap'
                },
                {
                    label: 'Scan Findings',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScanFindingList'
                    }),
                    icon: 'fa fa-scale-balanced'
                },
                {
                    label: 'Programs',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceProgramList'
                    }),
                    icon: 'fa fa-shield'
                },
                {
                    label: 'Tags',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceTagList'
                    }),
                    icon: 'fa fa-tags'
                },
                {
                    label: 'Scanning',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScanTaskList'
                    }),
                    icon: 'fa fa-binoculars'
                },
                {
                    label: 'Scanners',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScannerList'
                    }),
                    icon: 'fa fa-eye'
                },
                {
                    label: 'Scoping',
                    route: this.$router.resolve({
                        name: 'AttackSurfaceScopeList'
                    }),
                    icon: 'fa fa-compass'
                }
            ]
        };
    }
};
</script>

<template>
    <Navbar :items="items"></Navbar>
</template>
