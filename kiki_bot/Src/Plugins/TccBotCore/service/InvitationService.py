from ..database.UserMapper import User, UserMapper
from ..database.UserMCMapper import MCUser, UserMCMapper
from ..database.BanlistMapper import BanlistMapper, BanlistUser
from ..database.InvitationMapper import InvitationMapper
from ..utils import tools

class InvitationService:
    def add_relation(user_name_1, user_name_2):
        user_1 = UserMCMapper.get_user_by_name(user_name_1)
        if user_1 == None:
            raise tools.exception(f"{user_name_1} 不存在")
        
        user_2 = UserMCMapper.get_user_by_name(user_name_2)
        if user_2 == None:
            raise tools.exception(f"{user_name_2} 不存在")
        
        InvitationMapper.insert(user_2.id, user_1.id)
