<script>
import AuthLayout from '@/layout/AuthLayout.vue';

export default {
    name: '404',
    components: { AuthLayout }
};
</script>

<template>
    <AuthLayout title="" :hide-top-title="true">
        <div class="max-w-[95%] w-[95%] mx-auto">
            <div class="bg-surface-0 dark:bg-surface-900 py-10 px-8 sm:px-20 flex flex-col items-center" style="border-radius: 53px">
                <span class="text-primary font-bold text-6xl mb-6">404</span>
                <h1 class="text-surface-900 dark:text-surface-0 font-bold text-3xl lg:text-5xl mb-2">Not Found</h1>
                <div class="text-surface-600 dark:text-surface-200 mb-8">Requested resource is not available.</div>


                <Button as="router-link" label="Go to Dashboard" to="/" />
            </div>
        </div>
    </AuthLayout>
</template>

<style scoped></style>
