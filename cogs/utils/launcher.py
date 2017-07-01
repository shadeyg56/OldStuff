import json

def launch():
    config = open('cogs/utils/config.json').read()
    config = json.loads(config)
    print('-----------------------------------')
    print('Welcome to the KnightBot Launcher!')
    print('-----------------------------------')
    print('Please enter the following info: ')
    print('-----------------------------------')
    token = input('Bot Token \n> ')
    owner = input('Owner ID \n> ')
    prefix = input('Bot Prefix\n> ')
    admin = input('Admin Role \n> ')
    mod = input('Mod Role \n> ')
    admin_chat = input('Admin Chat \n> ')
    announcements = input('Announcement Channel \n> ')
    tournaments = input('Tournament Channel \n> ')
    print('-----------------------------------')
    print('Please wait while we input your data.')
    print('-----------------------------------')
    config['token'] = token
    config['owner'] = owner
    config['prefix'] = prefix
    config['admin_role'] = admin
    config['mod_role'] = mod
    config['admin_chat'] = admin_chat
    config['announcements'] = announcements
    config['tournaments'] = tournaments
    config['opened'] = 1

    if input('Launch Bot?\n> ').lower() == 'yes':
        config = json.dumps(config)
        with open('cogs/utils/config.json', 'w') as configfile:
            configfile.write(config)
        pass
    else:
        check()

def check():
    config = open('cogs/utils/config.json').read()
    config = json.loads(config)
    x = config['opened']
    if x == 0:
        x += 1
        config['opened'] = x
        launch()
    else:
        print('You have already set your configuration.')
        if input('Reset configuration?\n> ').lower() == 'yes':
            config['token'] = None
            config['owner'] = None
            config['prefix'] = None
            config['admin_role'] = None
            config['mod_role'] = None
            config['admin_chat'] = None
            config['announcements'] = None
            config['tournaments'] = None
            config['opened'] = 0

            config = json.dumps(config)

            with open('cogs/utils/config.json', 'w') as configfile:
                configfile.write(config)
            launch()
        else:
            pass


def settings():
    config = open("cogs/utils/config.json").read()
    config = json.loads(config)
    return config


