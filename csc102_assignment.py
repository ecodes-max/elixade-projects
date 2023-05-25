#creating a while loop to reconfirm password

#CREATE AN INPUT
#creating a funtion
import random
import string
def verified():
    n_attempts = 0
    #turn password into a global variable to be able to use outside the function
    global password
    global confirm_password
    password = input('CREATE YOUR PASSWORD ')
    global otp
    otp_ = str((random.randrange(1000,9999)))
    otp =  ''.join(otp_)
    print(f'YOUR OTP IS {otp} ')
    while n_attempts < 3:
    # confirming the password using a conditional statement
        confirm_password = input('CONFIRM THE PASSWORD YOU CREATED ')
        if password==confirm_password:
            print('YOUR PASSWORD HAS BEEN CREATED YOUR LOGIN DETAILS WILL BE SENT TO YOU  ')
            return
        else:
            print('Please put in the correct password')
            n_attempts += 1
    #creating a new conditional system for the recossion
            if n_attempts == 3:
                print('Try creating a memorable password')
                verified()
            continue
verified()
# the pin has been saved in variable password
# username for account will be randomized words
#import random for randomized string
#import string to create different string
def userlogin():
    u_name = (random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
    usercode = 'USER-'+''.join(u_name)
    main_password = input('INPUT IN YOUR PASSWORD ')
    in_otp = input('INPUT YOUR OTP ')
    if main_password == password and in_otp==otp :
        print(f"USERCODE : {usercode} \nPASSWORD : {main_password}  \nLOGIN DETAILS CONFIRMED ")
    else:
            print('put in the correct password or The right otp \nHINT in the otp give the space')
            userlogin()

userlogin()
