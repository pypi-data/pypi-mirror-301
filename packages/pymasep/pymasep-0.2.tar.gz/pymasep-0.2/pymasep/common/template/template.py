from pymasep.utils import native_xml_types, from_xml_types


class Template:
    """
    Template for a base object. A template is created from a dictionary

    name: name of the template
    name_base_object: name given to the created object if it is created from the template.
    If not given, name_base_object is set to name
    nature: the nature given the created object. May be None.
    created_class: the type of the BaseObject to create. Must be set
    value_type: for characteristics, the type of the value.
    default_value: default value for characteristic at the creation. May be none.
    subclass_template : name of sub template used to create sub BaseObject. These templates must already exist in the game
    controller: name of the class (full package name) to create a controller of an agent
    subclass_inheritance: list of template name used to inherit the subclass_templates

    :param game: The game where the template is created.
    :param template_dict: The dictionary used to create the template
    """

    def __init__(self, game, template_dict):
        self.name = template_dict['name']
        self.name_base_object = template_dict.get('name_base_object', self.name)
        self.nature = template_dict.get('nature')
        self.created_class = template_dict['created_class']
        self.value_type = native_xml_types.get(template_dict.get('value_type'),
                                               from_xml_types.get(template_dict.get('value_type')))
        self.default_value = template_dict.get('default_value')  # default value for characteristics
        self.subclass_templates = []
        self.game = game
        # for agents' templates
        self.controller = template_dict.get('controller')

        if 'subclass_templates' in template_dict:
            for tmplt_str in template_dict['subclass_templates']:
                self.subclass_templates.append(game.templates[tmplt_str])

        if 'subclass_inheritance' in template_dict:
            for tmplt_str in template_dict['subclass_inheritance']:
                other_template = game.templates[tmplt_str]
                for sub_tmpl in other_template.subclass_templates:
                    self.subclass_templates.append(sub_tmpl)
