#!/usr/bin/python
''' Uninstall script which will do following:
1. recovery lvm.conf.orig
2. recovery LVHDoISCSISR.py.orig
3. recovery pxssh.py.orig
4. delete RBDSR.py
5. recovery SR.py.orig
6. recovery mpath_dmp.py.orig
'''

import os, sys, shutil, subprocess


def usage():
    print("Usage:\n")
    print("[Command]")
    print("\t enable\tuninstall RBDSR")
    print("\t check\tCheck RBDSR")


def uninstall_rbdsr():
    print    ('########################################\nChecking if all files are in place:\n')
    
    path_sr = '/opt/xensource/sm/'
    path_python_lib = '/usr/lib/python2.4/site-packages/'
    path_lvm = '/etc/lvm/'
    b_rm_rcmodules = False

    if os.path.exists(path_sr + 'RBDSR.py'):
        print('#### found RBDSR.py                 ####')
    else:
        print('Couldn\'t find RBDSR.py here')
        sys.exit(1)
 
    if os.path.exists(path_sr + 'LVHDoISCSISR.py-orig'):
        print('#### LVHDoISCSISR.py-orig is here too ####')
    else:
        print('Couldn\'t find LVHDoISCSISR.py-orig here')
        sys.exit(1)

    if os.path.exists(path_lvm + 'lvm.conf-orig'):
        print('#### and lvm.conf-orig is here as well  ####')
    else:
        print('Couldn\'t find lvm.conf-orig here')
        sys.exit(1)
    
    if os.path.exists(path_sr + 'SR.py-orig'):
        print('#### SR.py-orig is here too ####')
    else:
        print('Couldn\'t find SR.py-orig here')
        sys.exit(1)
       
    if os.path.exists(path_sr + 'mpath_dmp.py-orig'):
        print('#### mpath_dmp.py-orig is here too ####')
    else:
        print('Couldn\'t find mpath_dmp.py-orig here')
        sys.exit(1)
    
    if os.path.exists(path_python_lib + 'pxssh.py-orig'):
        print('#### pxssh.py-orig is here too ####')
    else:
        print('Couldn\'t find pxssh.py-orig here')
        sys.exit(1)

    if os.path.exists('/etc/rc.modules-orig'):
        print('#### rc.modules-orig is here too ####')
    else:
        print('Couldn\'t find rc.modules-orig here')
        b_rm_rcmodules = True

    print('\n########################################\n\nUninstall RBDSR Starting:')

    if b_rm_rcmodules:
        # rm rc.modules
        os.remove('/etc/rc.modules')
    else:
        # recovery rc.modules
        shutil.move('/etc/rc.modules-orig','/etc/rc.modules')
    subprocess.call(["rmmod","rbd"])

    #current_path = os.path.dirname(os.path.realpath(__file__))
    # recovery pxssh.py
    shutil.move(path_python_lib + 'pxssh.py-orig', path_python_lib + 'pxssh.py')

    # recovery lvm.conf
    shutil.move(path_lvm + 'lvm.conf-orig', path_lvm + 'lvm.conf')
        
    # recovery LVHDoISCSISR.py
    shutil.move(path_sr + 'LVHDoISCSISR.py-orig', path_sr + 'LVHDoISCSISR.py') 
    
    # recovery RBDSR
    os.remove(path_sr + 'RBDSR.py')
    
    # recovery SR.py
    shutil.move(path_sr + 'SR.py-orig', path_sr + 'SR.py')
    
    # recovery mpath_dmp.py
    shutil.move(path_sr + 'mpath_dmp.py-orig', path_sr + 'mpath_dmp.py') 

    return True

def check_rbdsr():
    ret = False
    path_sr = '/opt/xensource/sm/'
    if os.path.exists(path_sr + 'RBDSR.py'):
        ret = True

    return ret

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    if sys.argv[1] == 'enable':
        ret = uninstall_rbdsr()
        if ret:
            print('Uninstall Success !\n')
    elif sys.argv[1] == 'check':
        ret = check_rbdsr()
        if ret:
            print('RBDSR Found')
        else:
            print('RBDSR NOT Found')
    
    sys.exit(0)

