from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template.context import make_context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode


class ContextMixin:
    def get_context_data(self, **kwargs):
        return kwargs


class TemplatedBaseMail(EmailMultiAlternatives, ContextMixin):
    template_name = None
    subject = None
    html = None

    _node_map = {
        'subject': 'subject',
        'text_body': 'body',
        'html_body': 'html',
    }

    def __init__(self, context=None, template_name=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = {} if context is None else context
        self.html = None

        if template_name is not None:
            self.template_name = template_name

    def get_template_name(self):
        if not self.template_name:
            raise ImproperlyConfigured("No template_name configured")
        return self.template_name

    def get_subject(self):
        if not self.subject:
            raise ImproperlyConfigured("No subject given!")
        return self.subject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**self.context)
        context["site_url"] = settings.SITE_URL
        context["site_name"] = settings.SITE_NAME
        return context

    def render(self):
        context = make_context(self.get_context_data())
        template = get_template(self.template_name)
        with context.bind_template(template.template):
            blocks = self._get_blocks(template.template.nodelist, context)
            for block_node in blocks.values():
                self._process_block(block_node, context)
        self._attach_body()

    def _process_block(self, block_node, context):
        attr = self._node_map.get(block_node.name)
        if attr is not None:
            setattr(self, attr, block_node.render(context).strip())

    def _get_blocks(self, nodelist, context):
        blocks = {}
        for node in nodelist:
            if isinstance(node, ExtendsNode):
                parent = node.get_parent(context)
                blocks.update(self._get_blocks(parent.nodelist, context))
        blocks.update({
            node.name: node for node in nodelist.get_nodes_by_type(BlockNode)
        })
        return blocks

    def _attach_body(self):
        if self.body and self.html:
            self.attach_alternative(self.html, 'text/html')
        elif self.html:
            self.body = self.html
            self.content_subtype = 'html'

    def send(self, to, *args, **kwargs):
        self.render()
        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        self.from_email = kwargs.pop(
            'from_email', settings.DEFAULT_FROM_EMAIL
        )
        super().send(*args, **kwargs)
        return True
