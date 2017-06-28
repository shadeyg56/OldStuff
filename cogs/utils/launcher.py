from configparser import ConfigParser  # ver. < 3.0
import os

config = ConfigParser()
config.read_file(open('cogs/utils/config.ini'))


def launch():
    config = ConfigParser()
    config.read_file(open('cogs/utils/config.ini'))
    print('-----------------------------------')
    print('Welcome to the KnightBot Launcher!')
    print('-----------------------------------')
    print('Please enter the following info: ')
    print('-----------------------------------')
    token = input('Bot Token \n> ')
    owner = input('Owner ID \n> ')
    admin = input('Admin Role \n> ')
    mod = input('Mod Role \n> ')
    prefix = input('Bot Prefix\n> ')
    print('-----------------------------------')
    print('Please wait while we input your data.')
    print('-----------------------------------')
    config.set('BOT', 'token', token)
    config.set('BOT', 'owner', owner)
    config.set('BOT', 'bot_prefix', prefix)
    config.set('COGS', 'admin_role', admin)
    config.set('COGS', 'mod_role', mod)
    config.set('LAUNCH', 'opened', '1')

    if input('Launch Bot?\n> ').lower() == 'yes':
        with open('cogs/utils/config.ini', 'w') as configfile:
            config.write(configfile)
        pass
    else:
        check()



def check():
    config = ConfigParser()
    config.read_file(open('cogs/utils/config.ini'))
    x = config.getint('LAUNCH','opened')
    if x == 0:
        x += 1
        config.set('LAUNCH', 'opened', str(x))
        launch()
    else:
        print('You have already set your configuration.')
        if input('Reset configuration?\n> ').lower() == 'yes':
            config.set('BOT', 'token', '')
            config.set('BOT', 'owner', '')
            config.set('COGS', 'admin_role', '')
            config.set('COGS', 'mod_role', '')
            config.set('LAUNCH', 'opened', '0')
            with open('cogs/utils/config.ini', 'w') as configfile:
                config.write(configfile)
            launch()
        else:
            pass
