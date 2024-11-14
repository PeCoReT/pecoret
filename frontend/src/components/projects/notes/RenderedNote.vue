<script>
export default {
    name: "RenderedNote",
    props: {
        note: {
            required: true
        }
    },
    data() {
        return {
            markdown: null
        }
    },
    methods: {
        renderMarkdown() {
            this.$api.post(this.$api.e.renderMarkdown, null, { markdown: this.note.text}).then((res) => {
                this.markdown = res.data.html
            })
        }
    },
    watch: {
        note: {
            deep: true,
            immediate: true,
            handler(value) {
                this.renderMarkdown()
            }
        }
    },
}
</script>

<template>
    <div class="renderedNote">
        <h4 class="text-3xl">{{ note.title }}</h4>

        <div v-html="this.markdown" class="checklist-description"></div>
    </div>
</template>

<style scoped>

</style>