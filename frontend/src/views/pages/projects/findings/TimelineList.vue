<script>
import { FindingTabMenu } from '@/partials/projects';
import ContainerLayout from '@/layouts/ContainerLayout.vue';

export default {
    name: 'TimelineList',
    data() {
        return {
            projectId: this.$route.params.projectId,
            findingId: this.$route.params.findingId,
            items: []
        };
    },
    methods: {
        getTimeline() {
            this.$api
                .get(this.$api.e.pFindingTimelineList, {
                    pPk: this.projectId,
                    fPk: this.findingId
                })
                .then((response) => {
                    this.items = response.data.results;
                });
        }
    },
    mounted() {
        this.getTimeline();
    },
    components: { ContainerLayout, FindingTabMenu }
};
</script>

<template>
    <ContainerLayout>
        <template #left-header>
            <FindingTabMenu></FindingTabMenu>
        </template>
        <div class="col-span-12 card mt-3">
            <div class="flex justify-center">
                <ol class="relative border-s border-muted-foreground">
                    <li class="mb-10 ms-6" v-for="item in items" :key="item.pk">
                        <span class="absolute flex items-center justify-center w-6 h-6 bg-primary rounded-full -start-3 ring-8 ring-gray-900">
                            <i class="text-primary-foreground fa fa-circle-dot text-xs"></i>
                        </span>
                        <h3 class="flex items-center mb-1 text-base font-semibold">
                            {{ item.title }}
                        </h3>
                        <time class="block mb-2 text-sm font-normal leading-none text-muted-foreground">
                            {{ item.date_created }}
                        </time>
                        <p class="mb-4 text-base font-normal text-muted">{{ item.text }}</p>
                    </li>
                </ol>
            </div>
        </div>
    </ContainerLayout>
</template>
