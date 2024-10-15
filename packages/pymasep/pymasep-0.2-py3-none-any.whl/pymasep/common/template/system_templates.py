SYSTEM_TEMPLATES = {
  "Templates": [
    {
      "name": "EmptyIntentionTemplate",
      "created_class": "Intention"
    },
    {
      "name": "EmptyBeliefTemplate",
      "created_class": "Belief"
    },
    {
      "name": "DefaultStateTemplate",
      "created_class": "State"
    },
    {
      "name": "GamePhase",
      "created_class": "Characteristic",
      "value_type": "str",
      "default_value": "play"
    },
    {
      "name": "SystemObjectStateTemplate",
      "created_class": "ObjectState",
      "subclass_templates": [
        "AgentOrder",
        "GamePhase"
      ]
    },
    {
      "name": "SystemObjectTemplate",
      "name_base_object": "system",
      "created_class": "Object",
      "subclass_templates": [
        "SystemObjectStateTemplate"
      ]
    },
    {
      "name": "SystemStateTemplate",
      "created_class": "State",
      "subclass_templates": [
        "SystemObjectTemplate"
      ]
    }
  ]
}
