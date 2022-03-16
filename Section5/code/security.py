from werkzeug.security import safe_str_cmp
from user import User

def authenticate(username,password):
    user = User.find_by_username(username)                          # username parameter : "jose", use the find_by_username method to retrieve the user by username
    if user is not None and safe_str_cmp(user.password,password):   # Then compare the password inside the user object with the typed password 
                                                                    # received through the /auth endpoint (user.password). 
                                                                    # The typed password is the password parameter pass to the
                                                                    # authenticate function
        return user                                                 # return user

def identity(payload):                                              # Payload argument is the contents of the JWT token
    user_id=payload['identity']                                     # Data stored inside a JWT is called a 'payload'. identity function
    return User.find_by_id(user_id)                                 # accepts the payload as parameter. 
                                                                    # The payload['identity'] contains the user's id property that we saved
                                                                    # into JWT when we created
                                                                    # For this case, payload['identity'] is 1, so user_id = 1
                                                                    # use the find_by_id method to retrieve the user by id, which is "jose"
                                                               


