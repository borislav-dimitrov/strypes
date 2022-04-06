class ShowAddUserCommand:
    def __init__(self, user_controller):
        self.user_controller = user_controller

    def __call__(self, *args, **kwargs):
        self.user_controller.show_add_user()
