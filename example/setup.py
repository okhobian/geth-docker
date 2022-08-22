import json
import subprocess
import secrets
import os.path
import shutil


config = {
    "network_id": 1399,
    "account_password": "primarypwd",
    "signers":{
        "passwords": ["password1","password2","password3"],
        "balances": ["2000", "2000", "2000"]
    },
    "bootnode_name": "geth-bootnode",
    "bootnode_port": 30303
}

def update_genesis(field, _data):
    
    try:
        with open("genesis.json", "r") as jsonFile:
            data = json.load(jsonFile)

        data[field] = _data

        with open("genesis.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
            
        return True, "UPDATED [genesis.json]: [{}] = [{}]".format(field, _data)
    
    except Exception as e:
        return False, str(e)

def update_dot_env(field, _data):
    
    try:
        with open(".env", "a") as file:
            file.write( f"{field}={_data}\n")
            
        return True, "UPDATED [.env]: [{}] = [{}]".format(field, _data)
    
    except Exception as e:
        return False, str(e)

def generate_bootnode_enode_addr(host, port):
    
    '''enode://ENODE@IP:PORT
        - host: bootnode service name in compose file, e.g., geth-bootnode
    '''
    
    try:
        ''' bootnode -genkey boot.key '''
        command = ["bootnode", "-genkey", "boot.key"]
        subprocess.run(command)
        # nodekey = secrets.token_hex(32) # 32 bytes -> 64 digits
        with open('boot.key') as f:
            nodekey = f.readline()
        
    except Exception as e:
        return "ERROR Gen boot.key" + str(e)
    
    try:
        port_str = f":{port}"
        # command = ["bootnode", "-nodekeyhex", str(nodekey), "-addr", port_str, "-writeaddress"]
        command = ["bootnode", "-nodekey", "boot.key", "-addr", port_str, "-writeaddress"]
        enode = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")
        enode = enode.strip('\n')
        print(enode)
        # return nodekey, f"enode://{enode}@{host}:0?discport={port}"
        return nodekey, f"enode://{enode}@{host}:{port}"
    
    except Exception as e:
        return "ERROR Gen enode" + str(e)

def extract_account_info(_info):
    
    if "Your new key was generated" not in _info:
        return

    for lines in _info.split("\n"):
        if "Public address of the key" in lines:
            public_addr = lines.strip().split(" ")[-1]
            
        if "Path of the secret key file" in lines:
            private_key_file = lines.strip().split(" ")[-1]
    
    return public_addr, private_key_file

def create_signers(passwords:list) -> list:
    
    signers = []
    
    # for every designated signers
    for password in passwords:
        
        # write each password to '/tmp/password'
        with open('/tmp/password', 'w') as f:
            f.write( str(password) )

        ## geth account new --password /tmp/password
        command = ['geth', 'account', 'new', '--password', '/tmp/password']
        result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        # extract public address & path to private key file from result
        public_addr, private_key_file = extract_account_info(result)
        
        # append to list
        signers.append([public_addr, private_key_file, str(password)])
    
    # rm -f /tmp/password
    subprocess.run(['rm', '-f', '/tmp/password'])
    
    return signers # list of ([public_addr, private_key_file, str(password)])

def compose_extra_data(signers):
    extra_data = "0x0000000000000000000000000000000000000000000000000000000000000000"
    for signer in signers:
        extra_data += signer[0][2:] # every signer's public address, exclude 0x
    extra_data += "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    
    return extra_data

def compose_alloc(signers, balances):
    
    alloc = {}
    for signer, balance in zip(signers, balances):
        alloc[ signer[0][2:] ] = { "balance": str(balance) }
    
    return alloc

def move_keystore_file_to_cur(signers):
    for signer in signers:
        shutil.move(signer[1], os.getcwd()) # move each private_key_file to current dir

        directory = os.listdir(os.getcwd()) # get all file names in current dir
        for fname in directory:
            # print("<<<<<< ", signer[0][2:])
            if str(signer[0][2:].lower()) in str(fname):    # signer has extra '0x' in the beginning
                print(">>>>>> ", fname, signer[0])
                os.rename(fname, signer[0][2:])              # rename private_key_file with public addr
                with open(f'{signer[0][2:]}.pwd', 'w') as f: # create password file for the account
                    f.write(signer[2])                       # write signer's password to file


if __name__ == '__main__':
    
    '''
        output_file: [.env] [genesis.json]
    '''

    ### [genesis.json] [.env] network id
    # result = update_genesis('config.chainId', config['network_id'])
    result = update_dot_env('NETWORK_ID', config['network_id'])
    print('[NETWORK_ID] updated') if result[0] else print(result[1])
    
    ### [.env] primary account
    result = update_dot_env('ACCOUNT_PASSWORD', config['account_password'])
    print('[ACCOUNT_PASSWORD] updated') if result[0] else print(result[1])

    ### [genesis.json] crate signers
    signers = create_signers(config['signers']['passwords'])
    print(signers)
    move_keystore_file_to_cur(signers)
    extra_data = compose_extra_data(signers)
    result = update_genesis('extradata', extra_data)
    print('[extra_data] updated') if result[0] else print(result[1])
    
    ### [.env] write signers to
    for i, signer in enumerate(signers, 1):
        result = update_dot_env("SIGNER_"+str(i), signer[0][2:])
        print('[signer] updated') if result[0] else print(result[1])
    
    ### [genesis.json] assign initial balances for each signer
    alloc = compose_alloc(signers, config['signers']['balances'])
    result = update_genesis('alloc', alloc)
    print('[alloc] updated') if result[0] else print(result[1])
    
    ### [.env] create bootnode [nodekey, enode]
    nodekey, enode = generate_bootnode_enode_addr(config['bootnode_name'], config['bootnode_port'])
    result = update_dot_env("NODE_KEY", nodekey)
    print('[nodekey] updated') if result[0] else print(result[1])
    result = update_dot_env("ENODE", enode)
    print('[enode] updated') if result[0] else print(result[1])