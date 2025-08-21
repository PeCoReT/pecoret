import MarkdownIt from 'markdown-it';

export default function renderMarkdown(markdown) {
    const md = MarkdownIt({});
    if (!markdown) {
        return '';
    }
    return md.render(markdown);
}
