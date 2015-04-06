import logging
from django.template import Library, Node, TemplateSyntaxError, Variable
from django.utils.safestring import mark_safe
from ..models import Param

register = Library()
logger = logging.getLogger('django_params')


class ParamNode(Node):
    def __init__(self, param_name, context_name):
        self.param_name = Variable(param_name)
        self.context_name = context_name

    def render(self, context):
        """
        Tag require `request` param into the context. So, check that
        'django.core.context_processors.request' is into TEMPLATE_CONTEXT_PROCESSORS
        and context for template was created as RequestContext(request, {<...>})
        """
        try:
            param = Param.get(context['request'], self.param_name.resolve(context))
            result = mark_safe(param.value)
            if self.context_name:
                context[self.context_name] = result
                return ""
            else:
                return result
        except Param.DoesNotExist as e:
            logger.warning(unicode(e))
            return ""

@register.tag
def param(parser, token):
    """
    DJANGO_PARAMS_NAME_CHOICES += (('(c)', 'Copyright'),)
    Param.objects.create(name='(c)',
                         value='(c) 2115, SuperCorp Inc.',
                         type=Param.TYPE_TEXT)
    In template:
    {% param '(c)' %} => '(c) 2115, SuperCorp Inc.'
    {% param '(c)' as copy %} => ''
    {% param '(c)' as copy %}{{ copy }} => (c) 2115, SuperCorp Inc.
    """
    tokens = token.split_contents()
    fnctl = tokens.pop(0)

    def error():
        raise TemplateSyntaxError, ("%s accepts the syntax: "
                "{%% %s param_name as context_name %%}, ") %(fnctl, fnctl)

    param_name = tokens.pop(0)
    context_name = None
    try:
        if tokens.pop(0) == 'as':
            context_name = tokens.pop(0)
    except IndexError:
        pass

    return ParamNode(param_name, context_name)
