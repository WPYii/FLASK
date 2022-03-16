from werkzeug.security import safe_str_cmp
from user import User
users=[
    User(1,'bob','asdf')
]

username_mapping={u.username : u for u in users}                    # Assigning key:value pair. So, u.username : u 
# username_mapping={'bob' : {                                                                     ,      'bob' : (1,'bob','asdf')
#     'id' : 1,
#     'username' : 'bob',
#     'password' : 'asdf'
#     }
# }

userid_mapping ={u.id : u for u in users}                           # Assigning key:value pair. So,  u.id : u 
# userid_mapping ={1: {                                                                           ,     1 : (1,'bob','asdf')
#     'id' : 1,
#     'username' : 'bob',
#     'password' : 'asdf'
#     }
# }

def authenticate(username,password):
    user = username_mapping.get(username,None)                      # username parameter:bob, use the username to find the correct user object
    if user is not None and safe_str_cmp(user.password,password):   # Then compare the password inside the user object with the typed password 
                                                                    # received through the /auth endpoint (user.password). 
                                                                    # The typed password is the password parameter pass to the
                                                                    # authenticate function
        return user                                                 # return user

def identity(payload):                                              # Payload argument is the contents of the JWT token
    user_id=payload['identity']                                     # Data stored inside a JWT is called a 'payload'. identity function
    return userid_mapping.get(user_id,None)                         # accepts the payload as parameter. 
                                                                    # The payload['identity'] contains the user's id property that we saved
                                                                    # into JWT when we created
                                                                    # For this case, payload['identity'] is 1, so user_id = 1
                                                                    # Then userid_mapping.get(user_id,None) will allow us to find the user,
                                                                    # which is Bob


