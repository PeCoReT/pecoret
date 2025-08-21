<script>
import {Skeleton} from "@/components/ui/skeleton";

export default {
    name: 'DefaultSkeleton',
    components: { Skeleton }
};
</script>

<template>
    <div class="flex items-center space-x-4">
        <Skeleton class="h-12 w-1/2 rounded" />
        <div class="space-y-2">
            <Skeleton class="h-4 my-3 w-[250px]" />
            <Skeleton class="h-4 w-[200px]" />
        </div>
    </div>
</template>
