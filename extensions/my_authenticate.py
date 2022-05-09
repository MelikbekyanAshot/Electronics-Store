from streamlit_authenticator import Authenticate
import streamlit as st
import datetime


class MyAuthenticate(Authenticate):
    def __init__(self, names, usernames, passwords, cookie_name, key, cookie_expiry_days=30):

        super().__init__(names, usernames, passwords, cookie_name, key, cookie_expiry_days)

    def login(self, form_name, button_name, login, password, location='main'):
        """Create a new instance of "authenticate".
        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of authenticated user.
        boolean
            The status of authentication, None: no credentials entered, False: incorrect credentials, True: correct credentials.
        str
            Username of authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        if not st.session_state['authentication_status']:
            self.token = self.cookie_manager.get(self.cookie_name)
            if self.token is not None:
                self.token = self.token_decode()
                if self.token is not False:
                    if not st.session_state['logout']:
                        if self.token['exp_date'] > datetime.utcnow().timestamp():
                            st.session_state['name'] = self.token['name']
                            st.session_state['authentication_status'] = True
                            st.session_state['username'] = self.token['username']

            if st.session_state['authentication_status'] != True:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(form_name)
                self.username = login_form.text_input(login)
                st.session_state['username'] = self.username
                self.password = login_form.text_input(password, type='password')

                if login_form.form_submit_button(button_name):
                    self.index = None
                    for i in range(0, len(self.usernames)):
                        if self.usernames[i] == self.username:
                            self.index = i
                    if self.index is not None:
                        try:
                            if self.check_pw():
                                st.session_state['name'] = self.names[self.index]
                                self.exp_date = self.exp_date()
                                self.token = self.token_encode()
                                self.cookie_manager.set(self.cookie_name, self.token,
                                                        expires_at=datetime.datetime.now() + datetime.timedelta(days=self.cookie_expiry_days))
                                st.session_state['authentication_status'] = True
                            else:
                                st.session_state['authentication_status'] = False
                        except Exception as e:
                            print(e)
                    else:
                        st.session_state['authentication_status'] = False
        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['username']
