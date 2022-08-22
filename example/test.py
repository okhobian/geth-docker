
# my_str='''
#         #10 1.449 
#         #10 1.449 Your new key was generated
#         #10 1.449 
#         #10 1.449 Public address of the key:   0x25dA50deD02Ad44569701E44Cc94C03732528967
#         #10 1.449 Path of the secret key file: /root/.ethereum/keystore/UTC--2022-07-23T17-12-12.149549670Z--25da50ded02ad44569701e44cc94c03732528967
#         #10 1.449 
#         #10 1.449 - You can share your public address with anyone. Others need it to interact with you.
#         #10 1.449 - You must NEVER share the secret key with anyone! The key controls access to your funds!
#         #10 1.449 - You must BACKUP your key file! Without the key, it's impossible to access account funds!
#         #10 1.449 - You must REMEMBER your password! Without the password, it's impossible to decrypt the key!
#         #10 1.449 
#         #10 1.449 
#         '''

# import re
# events = []

# print("Your new key was generated" in my_str)

# for item in my_str.split("\n"):
#     if "Public address of the key" in item:
#         result = item.strip().split(" ")
#         # print (item.strip())
#         print(result[-1])
        
#     if "Path of the secret key file" in item:
#         result = item.strip().split(" ")
#         # print (item.strip())
#         print(result[-1])
    

# for line in my_str:
    
#     match = re.search(r'Public address of the key', line)
#     if match:
#         events.append(match.group(1))
    
#     match = re.search(r'Path of the secret key file', line)
#     if match:
#         events.append(match.group(1))
        
# print(events)


# str = "0x7983D1527E3e24f7063B2076c23Ab1B651655d0a"
# print(str[2:])

