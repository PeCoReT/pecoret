import re

from attack_surface.models.target import Target
from attack_surface.models.scoping.item import ScopeItem
from attack_surface.models.target import ScopeChoices


def check_target_scope(target):
    """
    check if a target is in scope and return ScopeChoice

    Returns: `ScopeChoices`
    """
    program = target.program
    # get scopes for program
    scope_items = ScopeItem.objects.for_program(program)
    result = ScopeChoices.UNDEFINED
    # check if target is in excluded domains
    for item in scope_items.domains().excludes():
        if item.is_regex is True:
            # if regex matches our target data, we are out of scope
            if re.match(item.value, target.data):
                return ScopeChoices.OUT_OF_SCOPE
        # target is not regex, if it is a subdomain of excluded domain, return out of scope
        if target.data.endswith(f'.{item.value}') or target.data == item.value:
            target.scope = ScopeChoices.OUT_OF_SCOPE
            target.save()
            return ScopeChoices.OUT_OF_SCOPE
    for item in scope_items.domains().includes():
        if item.is_regex is True:
            if re.match(item.value, target.data):
                result = ScopeChoices.IN_SCOPE
                break
        else:
            if target.data.endswith(f'.{item.value}') or target.data == item.value:
                result = ScopeChoices.IN_SCOPE
                break
    target.scope = result
    target.save()
    return result


def check_scope_for_program(program):
    for target in Target.objects.for_program(program):
        check_target_scope(target)
