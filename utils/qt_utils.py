from PyQt6.QtCore import QObject

def find_child_by_type_and_id(parent: QObject, child_type: type, child_id: str) -> QObject:
    """
    Recursively search for a child QObject by its type and ID within the given parent QObject.

    :param parent: The parent QObject to start searching from.
    :param child_type: The type of child QObject to search for.
    :param child_id: The ID of the child QObject to search for.
    :return: The matching QObject if found, otherwise None.
    """
    # Check if the current object is of the desired type and has the desired ID
    if isinstance(parent, child_type) and parent.objectName() == child_id:
        return parent

    # Recursively search child objects
    for child in parent.findChildren(QObject):
        result = find_child_by_type_and_id(child, child_type, child_id)
        if result is not None:
            return result

    return None
