(define (domain upp)
(:requirements :typing)
(:types
  size_t - object
  location_t - object
  side_t - object
  color_t - object
  image_t - object
  resource_t - object
  sheet_t - object
)
(:constants letter - size_t black - color_t color - color_t front - side_t back - side_t some_feeder_tray - location_t some_finisher_tray - location_t endcap_entry-blackcontainer_exit - location_t htmoverblack_entry-endcap_exit - location_t htmoverblack_exit-down_topentry - location_t colorcontainer_entry-down_bottomexit - location_t colorcontainer_exittoime-colorprinter_entry - location_t colorprinter_exit-colorcontainer_entryfromime - location_t colorcontainer_exit-up_bottomentry - location_t down_bottomentry-colorfeeder_exit - location_t blackcontainer_entry-blackfeeder_exit - location_t down_topexit-htmovercolor_entry - location_t htmovercolor_exit-up_topentry - location_t blackcontainer_exittoime-blackprinter_entry - location_t blackprinter_exit-blackcontainer_entryfromime - location_t finisher1_entry-up_topexit - location_t finisher2_entry-finisher1_exit - location_t finisher1_tray - location_t finisher2_exit - location_t finisher2_tray - location_t endcap-rsrc - resource_t htmoverblack-rsrc - resource_t colorcontainer-rsrc - resource_t colorprinter-rsrc - resource_t colorfeeder-rsrc - resource_t blackfeeder-rsrc - resource_t down-rsrc - resource_t htmovercolor-rsrc - resource_t blackcontainer-rsrc - resource_t blackprinter-rsrc - resource_t up-rsrc - resource_t finisher1-rsrc - resource_t finisher2-rsrc - resource_t)
(:predicates
  (sheetsize ?sheet - sheet_t ?size - size_t)
  (location ?sheet - sheet_t ?location - location_t)
  (hasimage ?sheet - sheet_t ?side - side_t ?image - image_t)
  (sideup ?sheet - sheet_t ?side - side_t)
  (stackedin ?sheet - sheet_t ?location - location_t)
  (imagecolor ?image - image_t ?color - color_t)
  (notprintedwith ?sheet - sheet_t ?side - side_t ?color - color_t)
  (oppositeside ?side1 - side_t ?side2 - side_t)
  (available ?resource - resource_t)
  (prevsheet ?sheet1 - sheet_t ?sheet2 - sheet_t)
  (uninitialized)
)

(:action initialize
  :parameters ()
  :precondition (and (uninitialized))
  :effect (and
    (not (uninitialized))
    (available endcap-rsrc)
    (available htmoverblack-rsrc)
    (available colorcontainer-rsrc)
    (available colorprinter-rsrc)
    (available colorfeeder-rsrc)
    (available blackfeeder-rsrc)
    (available down-rsrc)
    (available htmovercolor-rsrc)
    (available blackcontainer-rsrc)
    (available blackprinter-rsrc)
    (available up-rsrc)
    (available finisher1-rsrc)
    (available finisher2-rsrc)
  )
)
(:action endcap-move-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available endcap-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet endcap_entry-blackcontainer_exit))
  :effect (and
    (not (available endcap-rsrc))
    (location ?sheet htmoverblack_entry-endcap_exit)
    (not (location ?sheet endcap_entry-blackcontainer_exit))
    (available endcap-rsrc)
  )
)
(:action htmoverblack-move-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available htmoverblack-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet htmoverblack_entry-endcap_exit))
  :effect (and
    (not (available htmoverblack-rsrc))
    (location ?sheet htmoverblack_exit-down_topentry)
    (not (location ?sheet htmoverblack_entry-endcap_exit))
    (available htmoverblack-rsrc)
  )
)
(:action colorcontainer-toime-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available colorcontainer-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet colorcontainer_entry-down_bottomexit))
  :effect (and
    (not (available colorcontainer-rsrc))
    (location ?sheet colorcontainer_exittoime-colorprinter_entry)
    (not (location ?sheet colorcontainer_entry-down_bottomexit))
    (available colorcontainer-rsrc)
  )
)
(:action colorcontainer-fromime-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available colorcontainer-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet colorprinter_exit-colorcontainer_entryfromime))
  :effect (and
    (not (available colorcontainer-rsrc))
    (location ?sheet colorcontainer_exit-up_bottomentry)
    (not (location ?sheet colorprinter_exit-colorcontainer_entryfromime))
    (available colorcontainer-rsrc)
  )
)
(:action colorprinter-simplex-letter
  :parameters (?sheet - sheet_t ?face - side_t ?image - image_t)
  :precondition (and
    (available colorprinter-rsrc)
    (sheetsize ?sheet letter)
    (sideup ?sheet ?face)
    (imagecolor ?image color)
    (location ?sheet colorcontainer_exittoime-colorprinter_entry)
    (notprintedwith ?sheet ?face color))
  :effect (and
    (not (available colorprinter-rsrc))
    (location ?sheet colorprinter_exit-colorcontainer_entryfromime)
    (hasimage ?sheet ?face ?image)
    (not (location ?sheet colorcontainer_exittoime-colorprinter_entry))
    (not (notprintedwith ?sheet ?face color))
    (available colorprinter-rsrc)
  )
)
(:action colorprinter-simplexmono-letter
  :parameters (?sheet - sheet_t ?face - side_t ?image - image_t)
  :precondition (and
    (available colorprinter-rsrc)
    (sheetsize ?sheet letter)
    (sideup ?sheet ?face)
    (imagecolor ?image black)
    (location ?sheet colorcontainer_exittoime-colorprinter_entry)
    (notprintedwith ?sheet ?face black))
  :effect (and
    (not (available colorprinter-rsrc))
    (location ?sheet colorprinter_exit-colorcontainer_entryfromime)
    (hasimage ?sheet ?face ?image)
    (not (location ?sheet colorcontainer_exittoime-colorprinter_entry))
    (not (notprintedwith ?sheet ?face black))
    (available colorprinter-rsrc)
  )
)
(:action colorfeeder-feed-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available colorfeeder-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet some_feeder_tray))
  :effect (and
    (not (available colorfeeder-rsrc))
    (location ?sheet down_bottomentry-colorfeeder_exit)
    (sideup ?sheet front)
    (not (location ?sheet some_feeder_tray))
    (available colorfeeder-rsrc)
  )
)
(:action blackfeeder-feed-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available blackfeeder-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet some_feeder_tray))
  :effect (and
    (not (available blackfeeder-rsrc))
    (location ?sheet blackcontainer_entry-blackfeeder_exit)
    (sideup ?sheet front)
    (not (location ?sheet some_feeder_tray))
    (available blackfeeder-rsrc)
  )
)
(:action down-movetop-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available down-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet htmoverblack_exit-down_topentry))
  :effect (and
    (not (available down-rsrc))
    (location ?sheet down_topexit-htmovercolor_entry)
    (not (location ?sheet htmoverblack_exit-down_topentry))
    (available down-rsrc)
  )
)
(:action down-movebottom-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available down-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet down_bottomentry-colorfeeder_exit))
  :effect (and
    (not (available down-rsrc))
    (location ?sheet colorcontainer_entry-down_bottomexit)
    (not (location ?sheet down_bottomentry-colorfeeder_exit))
    (available down-rsrc)
  )
)
(:action down-movedown-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available down-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet htmoverblack_exit-down_topentry))
  :effect (and
    (not (available down-rsrc))
    (location ?sheet colorcontainer_entry-down_bottomexit)
    (not (location ?sheet htmoverblack_exit-down_topentry))
    (available down-rsrc)
  )
)
(:action htmovercolor-move-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available htmovercolor-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet down_topexit-htmovercolor_entry))
  :effect (and
    (not (available htmovercolor-rsrc))
    (location ?sheet htmovercolor_exit-up_topentry)
    (not (location ?sheet down_topexit-htmovercolor_entry))
    (available htmovercolor-rsrc)
  )
)
(:action blackcontainer-toime-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available blackcontainer-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet blackcontainer_entry-blackfeeder_exit))
  :effect (and
    (not (available blackcontainer-rsrc))
    (location ?sheet blackcontainer_exittoime-blackprinter_entry)
    (not (location ?sheet blackcontainer_entry-blackfeeder_exit))
    (available blackcontainer-rsrc)
  )
)
(:action blackcontainer-fromime-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available blackcontainer-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet blackprinter_exit-blackcontainer_entryfromime))
  :effect (and
    (not (available blackcontainer-rsrc))
    (location ?sheet endcap_entry-blackcontainer_exit)
    (not (location ?sheet blackprinter_exit-blackcontainer_entryfromime))
    (available blackcontainer-rsrc)
  )
)
(:action blackprinter-simplex-letter
  :parameters (?sheet - sheet_t ?face - side_t ?image - image_t)
  :precondition (and
    (available blackprinter-rsrc)
    (sheetsize ?sheet letter)
    (sideup ?sheet ?face)
    (imagecolor ?image black)
    (location ?sheet blackcontainer_exittoime-blackprinter_entry)
    (notprintedwith ?sheet ?face black))
  :effect (and
    (not (available blackprinter-rsrc))
    (location ?sheet blackprinter_exit-blackcontainer_entryfromime)
    (hasimage ?sheet ?face ?image)
    (not (location ?sheet blackcontainer_exittoime-blackprinter_entry))
    (not (notprintedwith ?sheet ?face black))
    (available blackprinter-rsrc)
  )
)
(:action blackprinter-simplexandinvert-letter
  :parameters (?sheet - sheet_t ?face - side_t ?otherface - side_t ?image - image_t)
  :precondition (and
    (available blackprinter-rsrc)
    (sheetsize ?sheet letter)
    (oppositeside ?face ?otherface)
    (imagecolor ?image black)
    (location ?sheet blackcontainer_exittoime-blackprinter_entry)
    (notprintedwith ?sheet ?face black)
    (sideup ?sheet ?face))
  :effect (and
    (not (available blackprinter-rsrc))
    (location ?sheet blackprinter_exit-blackcontainer_entryfromime)
    (sideup ?sheet ?otherface)
    (hasimage ?sheet ?face ?image)
    (not (location ?sheet blackcontainer_exittoime-blackprinter_entry))
    (not (notprintedwith ?sheet ?face black))
    (not (sideup ?sheet ?face))
    (available blackprinter-rsrc)
  )
)
(:action up-movetop-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available up-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet htmovercolor_exit-up_topentry))
  :effect (and
    (not (available up-rsrc))
    (location ?sheet finisher1_entry-up_topexit)
    (not (location ?sheet htmovercolor_exit-up_topentry))
    (available up-rsrc)
  )
)
(:action up-moveup-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available up-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet colorcontainer_exit-up_bottomentry))
  :effect (and
    (not (available up-rsrc))
    (location ?sheet finisher1_entry-up_topexit)
    (not (location ?sheet colorcontainer_exit-up_bottomentry))
    (available up-rsrc)
  )
)
(:action finisher1-passthrough-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available finisher1-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet finisher1_entry-up_topexit))
  :effect (and
    (not (available finisher1-rsrc))
    (location ?sheet finisher2_entry-finisher1_exit)
    (not (location ?sheet finisher1_entry-up_topexit))
    (available finisher1-rsrc)
  )
)
(:action finisher1-stack-letter
  :parameters (?sheet - sheet_t ?prevsheet - sheet_t)
  :precondition (and
    (available finisher1-rsrc)
    (prevsheet ?sheet ?prevsheet)
    (location ?prevsheet some_finisher_tray)
    (sheetsize ?sheet letter)
    (location ?sheet finisher1_entry-up_topexit))
  :effect (and
    (not (available finisher1-rsrc))
    (location ?sheet some_finisher_tray)
    (stackedin ?sheet finisher1_tray)
    (not (location ?sheet finisher1_entry-up_topexit))
    (available finisher1-rsrc)
  )
)
(:action finisher2-passthrough-letter
  :parameters (?sheet - sheet_t)
  :precondition (and
    (available finisher2-rsrc)
    (sheetsize ?sheet letter)
    (location ?sheet finisher2_entry-finisher1_exit))
  :effect (and
    (not (available finisher2-rsrc))
    (location ?sheet finisher2_exit)
    (not (location ?sheet finisher2_entry-finisher1_exit))
    (available finisher2-rsrc)
  )
)
(:action finisher2-stack-letter
  :parameters (?sheet - sheet_t ?prevsheet - sheet_t)
  :precondition (and
    (available finisher2-rsrc)
    (prevsheet ?sheet ?prevsheet)
    (location ?prevsheet some_finisher_tray)
    (sheetsize ?sheet letter)
    (location ?sheet finisher2_entry-finisher1_exit))
  :effect (and
    (not (available finisher2-rsrc))
    (location ?sheet some_finisher_tray)
    (stackedin ?sheet finisher2_tray)
    (not (location ?sheet finisher2_entry-finisher1_exit))
    (available finisher2-rsrc)
  )
)
)