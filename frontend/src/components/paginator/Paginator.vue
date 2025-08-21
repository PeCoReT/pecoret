<script>
import { Pagination, PaginationEllipsis, PaginationFirst, PaginationLast, PaginationList, PaginationListItem, PaginationNext, PaginationPrev } from '@/components/ui/pagination';
import { Button } from '@/components/ui/button';

export default {
    name: 'Paginator',
    emits: ['page'],
    components: {
        Pagination,
        Button,
        PaginationEllipsis,
        PaginationFirst,
        PaginationLast,
        PaginationList,
        PaginationListItem,
        PaginationNext,
        PaginationPrev
    },
    props: {
        totalRecords: {
            required: true
        },
        rows: {
            required: true
        }
    },
    methods: {
        onPage(page) {
            this.$emit('page', page);
        }
    }
};
</script>

<template>
    <Pagination v-slot="{ page }" :items-per-page="rows" :sibling-count="1" :total="totalRecords" show-edges @update:page="onPage">
        <PaginationList v-slot="{ items }" class="flex items-center gap-1">
            <PaginationFirst />
            <PaginationPrev />

            <template v-for="(item, index) in items">
                <PaginationListItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                    <Button :variant="item.value === page ? 'default' : 'outline'" class="w-9 h-9 p-0">
                        {{ item.value }}
                    </Button>
                </PaginationListItem>
                <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <PaginationNext />
            <PaginationLast />
        </PaginationList>
    </Pagination>
</template>
