# SolarEdge input data and file management

import logging
import os
import select
import socket
import sys
import time

import serial

logger = logging.getLogger(__name__)
socketTimeout = 120.0
DATE_TOKEN = "__date__"


# open data sockets and wait for connection from inverter
def openDataSocket(ports):
    listeners = []
    # listen on all the specified ports
    for port in ports:
        logger.info("waiting for connection on port " + str(port))
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("", port))
        listener.listen(1)
        listeners.append(listener)
    # Wait for one of the listeners to get a client connection
    (readable, writable, exceptional) = select.select(listeners, [], [])
    listener = readable[0]
    (clientSocket, addr) = listener.accept()
    logger.info(
        "connection from %s:%s to port %d",
        addr[0],
        addr[1],
        listener.getsockname()[1],
    )
    # close all the listening sockets
    for listener in listeners:
        listener.close()
    # set a timeout so lost connection can be detected
    clientSocket.settimeout(socketTimeout)
    socketFile = clientSocket.makefile("rwb")
    socketFile.name = "<socket>"
    return socketFile


## open data socket and wait for connection from inverter
# def openDataSocket(sePort):
#    # open a socket and wait for a connection
#    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    dataSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#    dataSocket.bind(("", sePort))
#    dataSocket.listen(0)
#    logger.info("waiting for connection on port "+str(sePort))
#    (clientSocket, addr) = dataSocket.accept()
#    dataSocket.close()
#    logger.info("connection from %s:%s", addr[0], addr[1])
#    # set a timeout so lost connection can be detected
#    clientSocket.settimeout(socketTimeout)
#    return clientSocket.makefile("rwb")


# open serial device
def openSerial(inFileName, baudRate):
    return serial.Serial(inFileName, baudrate=baudRate)


def openInFile(inFileName):
    if inFileName == "stdin":
        return sys.stdin.buffer
    # Explicitly specify mode rb to keep Windows happy!
    return open(inFileName, "rb")


# close the data source
def closeData(dataFile, networkDevice):
    logger.info("closing %s", dataFile.name)
    dataFile.close()


# open the output file if it is specified
def openOutFile(fileName, writeMode="wb"):
    if fileName:
        fileName = fileName.replace(DATE_TOKEN, time.strftime("%Y%m%d"))
        dirName = os.path.dirname(fileName)
        if dirName:
            os.makedirs(dirName, exist_ok=True)
        if writeMode == "wb":
            fileName = nextFreeFileName(fileName)
        return open(fileName, writeMode)
    return None


# never overwrite an existing file, use 'name.1.ext', 'name.2.ext', etc. instead
def nextFreeFileName(fileName):
    if not os.path.isfile(fileName):
        return fileName
    (root, ext) = os.path.splitext(fileName)
    count = 1
    while os.path.exists("%s.%d%s" % (root, count, ext)):
        count += 1
    return "%s.%d%s" % (root, count, ext)


# close output files
def closeOutFiles(recFile, outFile):
    if recFile:
        logger.info("closing %s", recFile.name)
        recFile.close()
    if outFile:
        logger.info("closing %s", outFile.name)
        outFile.close()
