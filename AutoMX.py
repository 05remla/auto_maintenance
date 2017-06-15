# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:05:26 2017

@author: Leo
"""
import os, sys, time
from hybrid_shell import *
ProgDir    = os.path.dirname(os.path.realpath(__file__))
ConfigFile = '{}{}settings.conf'.format(ProgDir,os.path.sep)

def SETUP():
    with open(ConfigFile, 'w') as file:
        file.write('updater##\n')
        file.write('defragdevices##\n')
        file.write('cleaner##\n')
        file.write('defrag##\n')
        file.write('regbackup##\n')
        file.write('nasaddr##\n')
        file.write('acroscript##')
    print('setup complete.')

    
def INTERACTIVE():
    global _update
    global _defrag
    global _sys_bu
    global _reg_bu
    global _cleanr
    
    _update = input('Would you like to update packages? [YES\\no]: ')
    _defrag = input('Would you like to perform defragging? [YES\\no]: ')
    _sys_bu = input('Would you like to perform a system backup? [YES\\no]: ')
    _reg_bu = input('Would you like to perform a registry backup? [YES\\no]: ')
    _cleanr = input('Would you like to run ccleaner? [YES\\no]: ')


def RUN():
    global _update
    global _defrag
    global _sys_bu
    global _reg_bu
    global _cleanr
        
    if not os.path.isfile(ConfigFile):
        print('Config file does not exist. Exiting...')
        exit()
        
    with open(ConfigFile) as file:
        for line in file.readlines():
            key = line.split('#')[0]
            value = line.split('#')[1]
            if (key == 'updater'):
                Updater = value
            elif (key == 'defragdevices'):
                DefragDevices = value
            elif (key == 'cleaner'):
                Cleaner = value
            elif (key == 'defrag'):
                Defrag = value
            elif (key == 'regbackup'):
                RegBackup = value
            elif (key == 'nasaddr'):
                NASaddr = value
            elif (key == 'acroscript'):
                AcroScript = value
            else:
                print('{} is not a valid config entry. Exiting...'.format(key))
                print('try running {} --setup'.format(sys.argv))
                exit()
                
        
        
    if not (_reg_bu.lower() == 'no'):
        print('Creating registry backup...')
        time_stamp = time.strftime("%d-%m-%Y_%H-%M-%S")
        os.system('reg export "hkey_local_machine\\software\\microsoft\\windows" "{}{}regbackup_{}.reg"'.format(RegBackup, os.path.sep, time_stamp))

    if not (_update.lower() == 'no'):
        print('Updating packages...')
        os.system('"{}"'.format(Updater))

    if not (_cleanr.lower() == 'no'):
        print('Cleaning...')
        os.system('"{}" /AUTO'.format(Cleaner))

    if not (_defrag.lower() == 'no'):
        print('Defragging...')
        os.system('"{}" -o {}'.format(Defrag, DefragDevices))

    if not (_sys_bu.lower() == 'no'):
        os.chdir('C:\\ProgramData\\Acronis\\TrueImageHome\\Scripts')
        if hostUp(NASaddr):
            print('Creating system backup...')
            os.system('"C:\\Program Files (x86)\\Common Files\\Acronis\\TrueImageHome\\TrueImageHomeService.exe" /script:{}'.format(AcroScript))
            os.system('"C:\\Program Files (x86)\\Acronis\\TrueImageHome\\TrueImage.exe"')
        else:
            print('No NAS detected. Skipping system backup...')
            
    input('Complete.')


if __name__ == "__main__":
    global _update
    global _defrag
    global _sys_bu
    global _reg_bu
    global _cleanr
    
    if (len(sys.argv) >= 2):
        if (sys.argv[1] == "--auto"):
            _update = "YES"
            _defrag = "YES"
            _sys_bu = "YES"
            _reg_bu = "YES"
            _cleanr = "YES"
        elif (sys.argv[1] == "--setup"):
            SETUP()
            exit()
            
    if (len(sys.argv) == 1):
        INTERACTIVE()
        
    RUN()
