

class User:
    def __init__(self, qq_user_id, mc_user_name = None, mc_user_id = None, is_in_qq_group = None, banned_date = None):
        self.qq_user_id = qq_user_id
        self.mc_user_name = mc_user_name
        self.mc_user_id = mc_user_id
        self.is_in_qq_group = is_in_qq_group
        self.banned_date = banned_date

    def __repr__(self) -> str:
        return "打印 User 对象"
    
    def create_users_from_db(res) -> list:
        print(res)
        pass