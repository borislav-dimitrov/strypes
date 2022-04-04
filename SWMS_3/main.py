from model.service.startup_exit import start_up


# TODO
#   sample project in GIT at intro-python\09-library-mvc

def main():
    user_controller, warehousing_controller, sales_controller, logger = start_up()
    # warehousing_controller.print_all()


if __name__ == '__main__':
    main()
