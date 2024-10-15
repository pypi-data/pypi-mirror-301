from typing import Callable, Any
from types import MethodType
from copy import deepcopy

# Fonction permettant de servir d'initiateur aux objets.
def init(self, *args, **kwargs) -> None:
    for index, arg in enumerate(args):
        setattr(self, "attr%s" % index, arg)
    for key, value in kwargs.items():
        setattr(self, key, value)
    return

# Fonction gérant l'entrée du with.
def wEnter(self):
    return self

# Fonction gérant la sortie du with.
def wExit(self, executionType, executionValue, traceback):
    return self

# Fonction permettant de trouver une variable parmi les protos.
def find(self, value: str, default = None) -> Any | None:
    while True:
        if hasattr(self, value):
            return getattr(self, value)
        else:
            if not hasattr(self, "__parent__"):
                break
            self = self.__parent__
    return default

# Fonction gérant les appels de l'objet.
def decorator(self, *args, **kwargs):
    if hasattr(args[0], "__call__"):
        setattr(self, args[0].__name__, MethodType(args[0], self))
    else:
        o = deepcopy(self)
        o.new(*args, **kwargs)
        return o
    return self

# Fonciton permettant de convertir une Proto en un dictionnaire.
def protoToDict(proto: type) -> dict:
    o = (deepcopy(proto)).__dict__
    if hasattr(proto, "__parent__"):
        p = proto.__parent__.__dict__
        o = {**o, **p}
    o["__parent__"] = deepcopy(proto)
    return o

# Fonction permettant de créer les objets.
def proto(name: str, methodsOrProto: dict[str, Callable] = {}) -> type:
    if hasattr(methodsOrProto, "__isProto__") and getattr(methodsOrProto, "__isProto__", False) == True:
        methodsOrProto = protoToDict(methodsOrProto)
    o = type(name, (object,), {
        "__init__": init,
        "__call__": decorator,
        "__enter__": wEnter,
        "__exit__": wExit,
        "__isProto__": True,
        "find": find,
        **methodsOrProto
    })
    return o()
