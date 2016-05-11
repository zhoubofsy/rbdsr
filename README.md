# RBDSR - CEPH plugin for XenServer 6.5
This plugin automates creation and attaching RBD objects to XenServer as an SR. It creates LVM Volume group on top of the attached RBD object and then uses LVs as LVHD VDIs.

XenServer demo RBD SR, implemented as an extension of the exsiting iSCSI(LVHDoISCSISR) SR. It doesn't mean that it uses iSCSI per se, but rather forks iSCSI storage plugin operation path, to take advantage of creating SR from XenCenter.

In particular, after installing plugin, creating iSCSI SR with port 6789 will redirect code path to the RBDSR.py plugin and allow user to attach RBD object to XenServer and create LVM based SR on top of that object. While allowing RBD SR creation using XenCenter, this method doesn't impact LVHDoISCSISR.py in any other way, leaving iSCSI functionality otherwise unchanged. 

This plugin takes adventage of the following changes in XenServer 6.5. In this version of XenServer, an rbd module has been enbled on the kernel. As a result, RBD blocks can be attached to Dom0 with sysfs command:

```echo "$mons name=$name,secret=$secret $rbddev" > /sys/bus/rbd/add```

like the one described here: line 49 https://github.com/ceph/ceph-docker/blob/master/examples/coreos/rbdmap/rbdmap

Once the RBD block device is mapped, LVM SR can be created on top of it and shared across a XenServer pool.

## Install
Download latest version of the pluging to each host: https://eking-tech.eicp.net:4443/svn/cloud/src/rbdsr-xen-server

Now you can install/uninstall the RBDSR. 
Run `python ./install_rbdsr.py enable` on each host to patch all required files and copy RBDSR.py to `/opt/xensource/sm`.

## Uninstall
Run `python ./uninstall_rbdsr.py enable` on each host to uninstall.

## Check Status
Run `python ./uninstall_rbdsr.py check` on each host to check status.

## Usage

RBDSR.py extends iSCSI SR(lvmoiscsi) functionality to attach rbd images to the Dom0 and place LVHDs(VHD inside of LVM volume) VDIs on top of that block device.

Minimal requirements to create RBDSR are:
* target - IP address or hostname of the ceph monitor
* targetIQN - RBD pool name
* SCSIid - RBD image name
* chapuser - username of sudoer on ceph monitor
* chappassword - password of the ceph user
* port - monitor port number. currently only 6789 will divert LVHDoISCSISR into RBDSR


## Version

eg: 1.0.0

* 第一位，表示版本号
* 第二位，0：表示预发布版本；1：表示测试开发版本；2：表示稳定版本
* 第三位，feature、bugfix 版本号

### 版本号获取方法
RBDSR 安装成功后，在`opt/xensource/sm`目录下运行`python ./RBDSR.py version`查看当前版本号
