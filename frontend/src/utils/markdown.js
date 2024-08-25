import MarkdownIt from 'markdown-it';

function renderMarkdown(markdown) {
    const md = MarkdownIt({});
    return md.render(markdown);
}

export default { renderMarkdown };
