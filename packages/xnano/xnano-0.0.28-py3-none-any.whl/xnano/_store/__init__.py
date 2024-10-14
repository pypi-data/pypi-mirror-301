__all__ = [
    "Store",
]


from .._utils.helpers import router


class Store(router):
    pass


Store.init("zyx._store.store", "Store")
