from karton.core import Karton
class BHunters(Karton):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.log.warning("ssss")
    def dbconnect(self):
        print("ssqq")
        return "ww"
 