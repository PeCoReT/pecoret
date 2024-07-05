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
            this.$api.post("/render-markdown/", { markdown: this.note.text}).then((res) => {
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
    computed: {
        renderedContent() {
            this.$api.post("/render-markdown/", { markdown: this.note.text}).then((res) => {
                this.markdown = res.data.html
                return this.markdown
            })
        }
    }
}
</script>

<template>
    <div class="renderedNote">
        <h4>{{ note.title }}</h4>

        <div v-html="this.markdown"></div>

    </div>
</template>

<style scoped>

</style>