<script>
import { Navbar } from '@/components/navbar';

export default {
    name: 'KnowledgeBaseTabMenu',
    components: { Navbar },
    data() {
        return {
            items: [
                {
                    label: 'Vulnerability Templates',
                    icon: 'fa fa-bugs',
                    route: this.$router.resolve({
                        name: 'VulnerabilityTemplateList'
                    }).path
                },
                {
                    label: 'Technologies',
                    icon: 'fa fa-cogs',
                    route: this.$router.resolve({
                        name: 'TechnologyList'
                    }).path
                },
                {
                    label: 'Checklists',
                    icon: 'fa fa-circle-check',
                    route: this.$router.resolve({
                        name: 'ChecklistList'
                    })
                }
            ]
        };
    }
};
</script>

<template>
    <Navbar :items="items"></Navbar>
</template>
