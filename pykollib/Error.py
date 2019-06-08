from typing import Optional


class Error(Exception):
    def __init__(self, message: str, wait: Optional[int] = None) -> None:
        self.message = message
        self.wait = wait

    def __str__(self) -> str:
        return self.message


class ItemError(Error):
    def __init__(self, *args, item: Optional[int] = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.item = item


class LoginFailedGenericError(Error):
    pass


class LoginFailedBadPasswordError(Error):
    pass


class NightlyMaintenanceError(Error):
    pass


class NotLoggedInError(Error):
    pass


class RequestGenericError(Error):
    pass


class RequestFatalError(Error):
    pass


class InvalidActionError(Error):
    pass


class InvalidItemError(Error):
    pass


class InvalidOutfitError(Error):
    pass


class InvalidLocationError(Error):
    pass


class InvalidUserError(Error):
    pass


class ItemNotFoundError(ItemError):
    pass


class SkillNotFoundError(Error):
    pass


class EffectNotFoundError(Error):
    pass


class RecipeNotFoundError(Error):
    pass


class WrongKindOfItemError(Error):
    pass


class UserInHardcoreRoninError(Error):
    pass


class UserIsIgnoringError(Error):
    pass


class UserIsDrunkError(Error):
    pass


class UserIsFullError(Error):
    pass


class UserIsLowLevelError(Error):
    pass


class UserIsWrongProfessionError(Error):
    pass


class UserNotFoundError(Error):
    pass


class NotEnoughAdventuresError(Error):
    pass


class NotEnoughMeatError(Error):
    pass


class LimitReachedError(Error):
    pass


class AlreadyCompletedError(Error):
    pass


class BotRequestError(Error):
    pass


class QuestNotFoundError(Error):
    pass


class NotEnoughItemsError(Error):
    pass


class BannedFromChatError(Error):
    pass


class CannotChangeClanError(Error):
    pass


class ClanRaidsNotFoundError(Error):
    pass


class ClanPermissionsError(Error):
    pass


class UnknownError(Error):
    pass
