<script>
/*
Original source which only support vue2
https://raw.githubusercontent.com/F-loat/vue-simplemde/master/src/index.vue
*/
import EasyMDE from 'easymde';
import markdown from '@/utils/markdown';

export default {
    props: {
        modelValue: String,
        forceSync: {
            type: Boolean,
            default() {
                return true;
            }
        },
        highlight: {
            type: Boolean,
            default() {
                return true;
            }
        },
        sanitize: {
            type: Boolean,
            default() {
                return true;
            }
        },
        configs: {
            type: Object,
            default() {
                return {};
            }
        },
        showSaveButton: {
            default: false,
            type: Boolean
        }
    },
    emits: ['blur', 'update:modelValue', 'input', 'initialized', 'save'],
    data() {
        return {
            isValueUpdateFromInner: false,
            loading: false,
            value: this.modelValue,
            toolbar: ['bold', 'italic', 'heading', '|', 'quote', 'unordered-list', 'ordered-list', '|', 'link', '|', 'preview']
        };
    },
    mounted() {
        this.initialize();
    },
    methods: {
        initialize() {
            if (this.value === null) {
                this.value = '';
            }
            if (this.showSaveButton) {
                toolbar.push({
                    name: 'Save',
                    className: 'fa fa-save',
                    action: () => {
                        this.$emit('save');
                    }
                });
            }
            const configs = Object.assign(
                {
                    element: this.$el.firstElementChild,
                    initialValue: this.value,
                    previewRender: (plaintext) => {
                        // use markdown-it and sanitize values to prevent XSS
                        // the default copy&pasted code from the docs rendered
                        // `<img src=/X onerror=alert(document.domain)>`
                        return markdown.renderMarkdown(plaintext);
                    },
                    renderingConfig: {
                        codeSyntaxHighlighting: true
                    },
                    toolbar: this.toolbar,
                    promptURLs: false,
                    uploadImage: false,
                    maxHeight: '400px',
                    autofocus: false
                },
                this.configs
            );
            this.simplemde = new EasyMDE(configs);

            if (configs.initialValue) {
                this.$emit('update:modelValue', this.value);
            }
            this.bindingEvents();

            this.$nextTick(() => {
                this.$emit('initialized', this.simplemde);
            });
        },
        bindingEvents() {
            this.simplemde.codemirror.on('change', (instance, changeObj) => {
                if (changeObj.origin === 'setValue') {
                    return;
                }
                const val = this.simplemde.value();
                this.handleInput(val);
            });

            this.simplemde.codemirror.on('blur', () => {
                const val = this.simplemde.value();
                this.handleBlur(val);
            });
        },
        addPreviewClass(className) {
            const wrapper = this.simplemde.codemirror.getWrapperElement();
            const preview = document.createElement('div');
            wrapper.nextSibling.className += ` ${className}`;
            preview.className = `editor-preview ${className}`;
            wrapper.appendChild(preview);
        },
        handleInput(val) {
            this.isValueUpdateFromInner = true;
            this.$emit('update:modelValue', val);
            this.$emit('input', val);
        },
        handleBlur(val) {
            this.isValueUpdateFromInner = true;
            this.$emit('blur', val);
        }
    },
    unmounted() {
        this.simplemde = null;
    },
    watch: {
        modelValue(val) {
            if (this.simplemde === null) {
                this.initialize();
            }
            if (!this.forceSync && this.isValueUpdateFromInner) {
                this.isValueUpdateFromInner = false;
            } else {
                if (val === null) {
                    val = '';
                }
                this.value = val;
                if (this.isValueUpdateFromInner === true) {
                    const pos = this.simplemde.codemirror.getCursor();
                    this.simplemde.value(val);
                    this.simplemde.codemirror.setSelection(pos);
                } else {
                    this.simplemde.value(val);
                }
            }
        }
    }
};
</script>
<template>
    <div class="border-0 border-round">
        <textarea class="p-3" :value="modelValue" @blur="handleBlur($event.target.value)" @input="handleInput($event.target.value)" />
    </div>
</template>
<style>
@import '@/../node_modules/easymde/dist/easymde.min.css';

.CodeMirror {
    background: var(--surface-b) !important;
    color: inherit !important;
    border: 1px solid var(--surface-border) !important;
}

.editor-preview {
    background: var(--surface-b) !important;
    color: inherit !important;
}

.editor-toolbar button:hover {
    background-color: var(--surface-c) !important;
}

.editor-toolbar {
    border-top: 1px solid var(--surface-border);
    border-left: 1px solid var(--surface-border);
    border-right: 1px solid var(--surface-border);
}

.CodeMirror-cursor {
    border-left: 1px solid var(--text-color);
}

.editor-toolbar button.active,
.editor-toolbar button:hover {
    background-color: var(--surface-c);
    color: var(--text-color);
}

.CodeMirror .cm-spell-error:not(.cm-url):not(.cm-comment):not(.cm-tag):not(.cm-word) {
    background: inherit !important;
}

.CodeMirror-selected {
    background-color: var(--text-color-secondary) !important;
}

.editor-preview pre {
    background: var(--surface-a);
    padding: 1em;
}
</style>