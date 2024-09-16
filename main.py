from auth import AuthSystem

# Authsystem test

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    auth_system = AuthSystem()
    print(auth_system.register(username, password))
    
    print(auth_system.login(username, password))
    
    print(auth_system.logout())
    
    
    