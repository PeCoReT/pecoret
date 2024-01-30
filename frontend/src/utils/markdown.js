import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js';

function renderMarkdown(markdown) {
    const md = MarkdownIt({
        highlight: function (str, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(str, { language: lang }).value;
                } catch (error) {
                    console.log(error);
                }
            }
        }
    });
    return md.render(markdown);
}

export default { renderMarkdown };
