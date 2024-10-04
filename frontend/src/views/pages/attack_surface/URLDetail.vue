<script>
import ASMonitorService from '@/service/ASMonitorService';
import TechnologyMultiSelectField from '@/components/forms/fields/TechnologyMultiSelectField.vue';
import TagSelectField from '@/components/forms/fields/TagSelectField.vue';
import TechnologyBadge from '@/components/badges/TechnologyBadge.vue';
import TagBadgeButton from '@/components/badges/TagBadgeButton.vue';

export default {
    name: 'ScanFindingDetail',
    components: { TagBadgeButton, TechnologyBadge, TagSelectField, TechnologyMultiSelectField },
    data() {
        return {
            item: {},
            service: new ASMonitorService(),
            urlId: this.$route.params.urlId,
            breadcrumbs: [
                {
                    label: 'URLs',
                    to: this.$router.resolve({
                        name: 'AttackSurfaceURLList'
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
        this.getFinding();
    },
    methods: {
        confirmDialogDelete() {
            this.$confirm.require({
                message: 'Do you want to delete this url?',
                header: 'Delete Confirmation',
                icon: 'fa fa-trash',
                acceptClass: 'p-button-danger',
                accept: () => {
                    this.service.deleteURL(this.$api, this.urlId).then(() => {
                        this.$router.push({
                            name: 'AttackSurfaceURLList'
                        });
                    });
                }
            });
        },
        getFinding() {
            this.service.getURL(this.$api, this.urlId).then((response) => {
                this.item = response.data;
            });
        }
    }
};
</script>

<template>
    <BaseLayout :breadcrumbs="breadcrumbs">
        <template #pre-content-right>
            <div class="flex justify-end">
                <Button label="Delete" severity="danger" outlined icon="fa fa-trash" @click="confirmDialogDelete"></Button>
            </div>
        </template>
        <div class="col-span-12 card">
            <h2 class="text-2xl font-semibold mb-2">URL: {{ item.url }}</h2>
            <p class="mb-2"><strong>Status Code:</strong> {{ item.status_code }}</p>
            <div id="technologies" v-if="item.technologies && item.technologies.length > 0">
                <p class="mb-4"><strong>Technologies:</strong></p>
                <div class="flex flex-wrap space-x-2 mb-4">
                    <TechnologyBadge :technology-name="technology.name" v-for="technology in item.technologies" :key="technology.pk" :disableHover="true"></TechnologyBadge>
                </div>
            </div>

            <div id="tags" v-if="item.tags && item.tags.length > 0">
                <p class="mb-2"><strong>Tags:</strong></p>
                <TagBadgeButton :label="tag" v-for="tag in item.tags" :key="tag.pk"></TagBadgeButton>
            </div>

            <div class="mt-3" v-if="item.response">
                <h3 class="text-xl font-semibold mb-2">Response</h3>
                <div class="card bg-surface-950">
                    <code style="white-space: pre-wrap">{{ item.response.slice(0, 2000) }}</code>
                </div>
            </div>
        </div>
    </BaseLayout>
</template>
