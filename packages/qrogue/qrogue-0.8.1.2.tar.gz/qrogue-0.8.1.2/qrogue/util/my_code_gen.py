
__PREFIX = "def __init__(self,"


def gen_class(class_name: str, constructor: str) -> str:
    og_constructor = constructor    # store for debugging
    start = constructor.index(__PREFIX)
    constructor = constructor[start:]   # get rid of everything before the constructor
    if not constructor.endswith(":"): constructor += ":"
    end = constructor.rfind("):")
    parameters = constructor[len(__PREFIX):end].split(",")

    class_text = f"class {class_name}:\n"
    constructor_lines = []
    property_lines = []
    for val in parameters:
        property_lines.append("@property")
        if ":" in val:
            type_start = val.index(":")
            param_name = val[:type_start].strip()
            param_type = val[type_start+1:].strip()
            property_lines.append(f"def {param_name}(self) -> {param_type}:")
        else:
            param_name = val.strip()
            property_lines.append(f"def {param_name}(self):")
        constructor_lines.append(f"self.__{param_name} = {param_name}")
        property_lines.append(f"\treturn self.__{param_name}")
        property_lines.append("")

    constructor_text = f"\t{constructor}\n" \
                       + "\n".join([f"\t\t{ctr}" for ctr in constructor_lines]) \
                       + "\n\n"

    property_text = "\t" + "\n\t".join(property_lines)

    return class_text + constructor_text + property_text


if __name__ == "__main__":
    t = gen_class("MapMetaData",
                  "def __init__(self, name: Optional[str], description: Optional[Message], has_teleporter: bool, show_description: Callable, show_individual_qubits: bool = False, end_message: Optional[Message] = None)")
    print(t)
