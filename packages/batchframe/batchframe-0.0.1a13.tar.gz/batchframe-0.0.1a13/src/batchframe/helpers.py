from importlib.metadata import version, PackageNotFoundError

def get_all_inheritors(clazz: type):
    subclasses: set[type] = set()
    parents: list[type] = [clazz]
    while parents:
        parent = parents.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                parents.append(child)
    return subclasses

def get_version() -> str:
    result = "UNKNOWN VERSION"
    found = False
    try:
        from batchframe import _version #type: ignore # File is generated at build-time
        result = "v" + _version.version
        found = True
    except ImportError:
        pass

    if not found:
        try:
            result = "v" + version('batchframe')
            found = True
        except PackageNotFoundError:
            pass
    
    return result