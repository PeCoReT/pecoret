<script>
import AppTopbar from '@/partials/AppTopbar.vue';
import Toaster from '@/components/ui/toast/Toaster.vue';
import {ConfirmDialog} from "@/components/dialog";

export default {
    components: {AppTopbar, Toaster, ConfirmDialog}
}

</script>
<template>
    <div class="bg-background flex min-h-screen min-w-[100] overflow-hidden">
        <div class="w-screen">
            <app-topbar></app-topbar>
            <div class="max-w-[95%] w-[95%] mx-auto">
                <Toaster />

                <ConfirmDialog ref="confirmDialog"></ConfirmDialog>
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>
