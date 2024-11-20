<script setup>
import AppTopbar from '@/components/navigation/bars/AppTopbar.vue';
</script>
<template>
    <div class="bg-surface-50 dark:bg-surface-950 flex min-h-screen min-w-[100] overflow-hidden">
        <div class="w-screen">
            <app-topbar></app-topbar>
            <div class="max-w-[95%] w-[95%] mx-auto">
                <Toast />
                <ConfirmDialog></ConfirmDialog>
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>
