def get_nested_technologies(instance):
    already_checked = set()
    tech_queue = set()
    for technology in instance.technologies.all():
        already_checked.add(technology)
        tech_queue.add(technology)
        for implicit_tech in technology.implicit_technologies.all():
            tech_queue.add(implicit_tech)
        while len(tech_queue) > 0:
            tech = tech_queue.pop()
            already_checked.add(tech)
            for implicit_tech in tech.implicit_technologies.all():
                if implicit_tech not in already_checked:
                    tech_queue.add(implicit_tech)
    return already_checked
