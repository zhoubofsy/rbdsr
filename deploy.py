#!/usr/bin/python
''' Install script which will do following:
1. add modprobe rbd to rc.modules
2. patch lvm.conf to detect volumes on rbd block devices
3. patch LVHDoISCSISR.py to redirect port 6789 requests to RBDSR.py
4. patch pxssh.py to allow remote commands
5. copy RBDSR.py to /opt/xensource/sm
6. patch SR.py
7. patch mpath_dmp.py
'''

''' Uninstall script which will do following:
1. recovery lvm.conf.orig
2. recovery LVHDoISCSISR.py.orig
3. delete RBDSR.py
4. recovery SR.py.orig
5. recovery mpath_dmp.py.orig
'''

import os, sys, shutil, subprocess


ins_files = ['RBDSR.py', 'LVHDoISCSISR.patch', 'lvm.patch', 'lvm-master.patch', 'pxssh.py', 'pexpect.py', 'SR.patch', 'mpath_dmp.patch']

path_sr = '/opt/xensource/sm'
path_python_lib = '/usr/lib/python2.7/site-packages'
path_lvm = '/etc/lvm'
current_path = os.path.dirname(os.path.realpath(__file__))

unins_files = ['%s/RBDSR.py' % path_sr, '%s/LVHDoISCSISR.py-orig' % path_sr, '%s/lvm.conf-orig' % path_lvm, '%s/SR.py-orig' % path_sr, '%s/mpath_dmp.py-orig' % path_sr]

def usage():
    print "Usage: %s < check | install | uninstall | clean >" % (sys.argv[0])

def clean_file(target):
    if os.path.exists(target):
        os.remove(target)
        print('remove -> %s' % target)


def check_file(ck_file):
    ck_result = False
    if os.path.exists(ck_file):
        ck_result = True
    else:
        print('Couldn\'t find %s' % ck_file)
    return ck_result

def check_file_list(ck_file_list):
    ck_result = True
    for item in ck_file_list:
        if not check_file(item):
            ck_result = False
            break
    return ck_result

def install():
    print('Enabling rbd driver on boot via rc.modules')
    '''TODO: should check if rbd is already in the rc.modules before writing it''' 
    try:
        rcfile = open('/etc/rc.modules','a')
        rcfile.write('\nmodprobe rbd\n')
        rcfile.close()
        subprocess.call(["modprobe","rbd"])
    except IOError, e:
        print 'Was unable to add rbd to rc.modules. Error: %s' % e
        sys.exit(1)
   
    try:
        os.chmod('/etc/rc.modules', 0744)
    except OSError, e:
        print 'Couldn\'t set execute permissions to rc.modules. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)
    
    os.chdir('/usr/lib/python2.7/site-packages/')
    shutil.copy('%s/pxssh.py' % current_path, 'pxssh.py')
    shutil.copy('%s/pexpect.py' % current_path, 'pexpect.py')
 
    os.chdir('/etc/lvm/')
    shutil.copy('lvm.conf','lvm.conf-orig')
    try:
        subprocess.call(["patch", "-f", "lvm.conf", "%s/lvm.patch" % current_path])
        os.chdir('/etc/lvm/master')
        shutil.copy('lvm.conf','lvm.conf-orig')
        subprocess.call(["patch", "-f", "lvm.conf", "%s/lvm-master.patch" % current_path])
        print('....\nlvm.conf is patched')
    except OSError, e:
        print 'Couldn\'t patch lvm.conf. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)

    os.chdir('/opt/xensource/sm')
    shutil.copy('LVHDoISCSISR.py','LVHDoISCSISR.py-orig') 
    try:
        subprocess.call(["patch", "-f", "LVHDoISCSISR.py", "%s/LVHDoISCSISR.patch" % current_path])
        print('....\nLVHDoISCSISR.py is patched')
    except OSError, e:
        print 'Couldn\'t patch LVHDoISCSISR.py. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)
    
    try:
        shutil.copyfile(current_path + '/RBDSR.py', 'RBDSR.py')
    except OSError, e:
        print 'Couldn\'t copy RBDSR.py. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)
    print('....\nRBDSR.py has been copied to /opt/xensource/sm')
    
    try:
        shutil.copy('scsiutil.py', 'scsiutil.py-orig')
        subprocess.call(["patch", "-f", "scsiutil.py", "%s/scsiutil.patch" % current_path])
        print '....\nscsiutil.py is patched'
    except OSError, e:
        print 'Couldn\'t patch scsiutil.py. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)

    try:
        shutil.copy('SR.py', 'SR.py-orig')
        subprocess.call(["patch", "-f", "SR.py", "%s/SR.patch" % current_path])
        print '....\nSR.py is patched'
    except OSError, e:
        print 'Couldn\'t patch SR.py. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)

    try:
        shutil.copy('mpath_dmp.py', 'mpath_dmp.py-orig')
        subprocess.call(["patch", "-f", "mpath_dmp.py", "%s/mpath_dmp.patch" % current_path])
        print '....\nmpath_dmp.py is patched'
    except OSError, e:
        print 'Couldn\'t patch mpath_dmp.py. Error: %s [errno=%s]' % (e.args)
        sys.exit(1)

def uninstall():

    print('\n########################################\n\nUninstall RBDSR Starting:')

    if not os.path.exists('/etc/rc.modules-orig'):
        # rm rc.modules
        clean_file('/etc/rc.modules')
    else:
        # recovery rc.modules
        shutil.move('/etc/rc.modules-orig','/etc/rc.modules')
    subprocess.call(["rmmod","rbd"])

    # recovery lvm.conf
    subprocess.call(["patch", "-f", "-R", "%s/lvm.conf" % path_lvm, "%s/lvm.patch" % current_path])
    subprocess.call(["patch", "-f", "-R", "%s/master/lvm.conf" % path_lvm, "%s/lvm-master.patch" % current_path])
        
    # recovery LVHDoISCSISR.py
    subprocess.call(["patch", "-f", "-R", "%s/LVHDoISCSISR.py" % path_sr, "%s/LVHDoISCSISR.patch" % current_path])
    
    # recovery RBDSR
    clean_file('%s/RBDSR.py' % path_sr)

    # recovery scsiutil.py
    subprocess.call(["patch", "-f", "-R", "%s/scsiutil.py" % path_sr, "%s/scsiutil.patch" % current_path])
    
    # recovery SR.py
    subprocess.call(["patch", "-f", "-R", "%s/SR.py" % path_sr, "%s/SR.patch" % current_path])
    
    # recovery mpath_dmp.py
    subprocess.call(["patch", "-f", "-R", "%s/mpath_dmp.py" % path_sr, "%s/mpath_dmp.patch" % current_path])

def clean_env():
    print("\n#####################################\n\nClean '*-orig' file: \n")
    clean_file('/etc/lvm/lvm.conf-orig')
    clean_file("/etc/lvm/master/lvm.conf-orig")
    clean_file("/opt/xensource/sm/LVHDoISCSISR.py-orig")
    clean_file("/opt/xensource/sm/scsiutil.py-orig")
    clean_file("/opt/xensource/sm/SR.py-orig")
    clean_file("/opt/xensource/sm/mpath_dmp.py-orig")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    if 'check' == sys.argv[1]:
        if check_file_list(unins_files):
            print 'RBDSR Installed'
        else:
            print 'RBDSR Uninstalled'
    elif 'install' == sys.argv[1]:
        if not check_file_list(ins_files):
            sys.exit(1)
        install()
        print 'Success !'
    elif 'uninstall' == sys.argv[1]:
        if not check_file_list(unins_files):
            sys.exit(1)
        if not check_file_list(ins_files):
            sys.exit(1)
        uninstall()
        print 'Success !'
    elif 'clean' == sys.argv[1]:
        clean_env()
        print 'Done !'
    else:
        usage()
        
    sys.exit(0)

