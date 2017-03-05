from .united_states import UnitedStates
from .canada import Canada
from .united_kingdom import UnitedKingdom

US = UnitedStates()
CA = Canada()
UK = UnitedKingdom()


def Fees(marketplace="US"):
    """Factory function returns class corresponding to country """

    factory = {"US": UnitedStates, "CA": Canada, "UK": UnitedKingdom}

    return factory[marketplace]()
