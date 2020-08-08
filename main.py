import clr

import serial
import struct
import time

import sys, os, traceback, types

file = 'OpenHardwareMonitorLib'
clr.AddReference(file)
from OpenHardwareMonitor import Hardware

def isUserAdmin():

    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print ("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise (RuntimeError, "Unsupported operating system for this module: %s" % (os.name,))

def runAsAdmin(cmdLine=None, wait=True):

    if os.name != 'nt':
        raise (RuntimeError, "This function is only implemented on Windows.")

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
        raise (ValueError, "cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)
    # XXX TODO: isn't there a function or something we can call to massage command line params?
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        #print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc


if not isUserAdmin():
    runAsAdmin()

def CpuHandle():
    handle = Hardware.Computer()
    handle.CPUEnabled = True
    handle.Open()
    return handle

def GpuHandle():
    handle = Hardware.Computer()
    handle.GPUEnabled = True
    handle.Open()
    return handle

def getDeviceIndex(handle):

    for i in range(len(handle.Hardware)):
        handle.Hardware[i].Update()
        for x in range(len(handle.Hardware[i].Sensors)):
            sensor = handle.Hardware[i].Sensors[x]
            if (sensor.Name == "CPU Package" and sensor.SensorType == 2 or sensor.Name == "GPU Core" and sensor.SensorType == 2):
                print(sensor.Name, sensor.Value)
                print(i, x)
            #break


def getCpuTemp(handle):
    handle.Hardware[0].Update()
    return int(handle.Hardware[0].Sensors[15].Value)
def getGpuTemp(handle):
    handle.Hardware[0].Update()
    return int(handle.Hardware[0].Sensors[0].Value)

HardwareHandle = CpuHandle()

getDeviceIndex(GpuHandle())
#print(getCpuTemp(HardwareHandle))

while True:
    while True:
        try:
            time.sleep(1)
            ser1 = serial.Serial('COM4', 9600)
            break
        except:
            pass
    print("connected")
    while True:
        try:
            ser1.write(struct.pack('>bb',int(getGpuTemp(GpuHandle())), int(getCpuTemp(HardwareHandle))))
            while True:
                time.sleep(0.1)
                serVstup = ser1.readline()
                #print(serVstup[0])
                if serVstup[0] == 98:
                    break;
        except:
            break
