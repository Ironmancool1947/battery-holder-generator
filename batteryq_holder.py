# battery-holder-generator

import cadquery as cq

def make_battery_holder(type="AA", count=5, wall_mount=True):
    sizes = {
        "AA": (14.5, 50),
        "AAA": (10.5, 44)
    }
    diameter, height = sizes[type]
    spacing = diameter + 3  # space between batteries
    holder_width = spacing * count
    holder_height = diameter * 2
    holder_depth = 20

    # Create the main block
    holder = cq.Workplane("XY").box(holder_width, holder_height, holder_depth)

    # Add battery holes
    start_x = -holder_width / 2 + spacing / 2
    for i in range(count):
        x = start_x + i * spacing
        holder = holder.faces(">Z").workplane(centerOption="CenterOfMass").pushPoints([(x, 0)]).hole(diameter)

    # Optional wall mount holes
    if wall_mount:
        screw_offset = 10
        screw_diameter = 4
        holder = holder.faces(">Z").workplane(centerOption="CenterOfMass").pushPoints([
            (-holder_width / 2 + screw_offset, holder_height / 2 - screw_offset),
            (holder_width / 2 - screw_offset, holder_height / 2 - screw_offset)
        ]).hole(screw_diameter)

    return holder

# Generate the model
model = make_battery_holder("AA", 5, wall_mount=True)

# Export to STL
cq.exporters.export(model, "battery_holder_AA_5_wallmount.stl")


