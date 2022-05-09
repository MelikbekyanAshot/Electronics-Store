from application.application import Application
from application.admin_application import AdminApplication
from application.consumer_application import ConsumerApplication


if __name__ == '__main__':
    Application.set_config()
    auth_status, user_name = Application.login_form()
    if auth_status and user_name == 'admin':
        AdminApplication.run()
    elif auth_status and user_name != 'admin':
        app = ConsumerApplication(user_name)
        app.run()
