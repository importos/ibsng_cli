arguments=[
    ("username","text"),
    ("password","password"),
]
def call(ibsapi,arguments):
    ibsapi.set_session(None)
    res,_ = ibsapi.login.login(
        auth_name= "anonymous",
        auth_pass= "anonymous",
        auth_type= "ANONYMOUS",
        login_auth_name=arguments["username"],
        login_auth_pass=arguments["password"],
        login_auth_type="ADMIN",
        create_session=True,
        auth_remoteaddr="1.1.1.1",
        is_https=False
    )
    ibsapi.set_session(res)
    return res