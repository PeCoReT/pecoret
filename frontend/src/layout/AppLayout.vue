<script setup>
import AppTopbar from './AppTopbar.vue';

</script>

<template>
    <div class="layout-wrapper layout-static">
        <app-topbar></app-topbar>

        <div class="p-container-fluid">
            <div class="layout-main">
                <Toast />
                <ConfirmDialog></ConfirmDialog>

                <router-view></router-view>
            </div>
        </div>
        <div class="layout-mask"></div>
    </div>
</template>
