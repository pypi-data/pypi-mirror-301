from pygame.event import custom_type

# Board Events
SQUARE_SELECTED_EVENT = custom_type()
""" Board event : A square has been selected """

SQUARE_VALIDATION_EVENT = custom_type()
""" Board event : A list of squares has been validate """

# Init window Event

INIT_WINDOW_VALIDATION_EVENT = custom_type()
""" Init windows event : all inputs have been validated """

MERCHANT_ADD_OBJECT_EVENT = custom_type()
""" Merchant event : the ADD button is pressed """

MERCHANT_REMOVE_OBJECT_EVENT = custom_type()
""" Merchant event : the REMOVE button is pressed """

# video events

VIDEO_ENDED_EVENT = custom_type()
""" Video is ended (by user or end of frames)"""

# Talk events

INTENTION_TALK_EVENT = custom_type()
""" Intention for talking event """

TALK_EVENT = custom_type()
""" Talk event : a player chose what he says """

