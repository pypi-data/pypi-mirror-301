__all__ = ["Store"]


from .._router import router


class Store(router):
    pass


Store.init("xnano.stores.store", "Store")