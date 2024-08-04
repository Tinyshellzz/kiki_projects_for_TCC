from ..database.UserMapper import User, UserMapper
from ..database.UserMCMapper import MCUser, UserMCMapper
from ..database.BanlistMapper import BanlistMapper, BanlistUser
from ..database.InvitationMapper import InvitationMapper
from ..utils import tools

class UserService:
    def get_by_qq_or_name(key: str):
        userbyname = UserMCMapper.get(user_name=key)
        if userbyname != None: return userbyname

        userbyqq = UserMCMapper.get(qq_num=key)
        return userbyqq
        
