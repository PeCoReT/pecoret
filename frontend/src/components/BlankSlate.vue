<script>
export default {
    name: 'BlankSlate',
    props: {
        icon: {
            required: true
        },
        title: {
            required: true
        },
        text: {
            required: true
        }
    }
};
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="flex flex-column text-center">
                <div class="align-center p-8">
                    <p>
                        <i :className="this.icon + ' fa-2x'"></i>
                    </p>
                    <h3>{{ this.title }}</h3>
                    <p class="text-disabled mt-3">
                        {{ this.text }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
