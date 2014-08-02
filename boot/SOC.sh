#!/bin/sh
format=1.0
board=am335x_evm

bootloader_location=fatfs_boot
dd_spl_uboot_seek=
dd_spl_uboot_bs=
dd_uboot_seek=
dd_uboot_bs=

conf_bootcmd=
boot_script=
boot_fstype=fat
conf_boot_startmb=1
conf_boot_endmb=96
sfdisk_fstype=0xE

serial_tty=ttyO0
fdtfile=

usbnet_mem=

