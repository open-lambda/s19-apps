import json
import pickle

from core import lampy as np, Client, delay

# # Client/Server unsingleton identity
# client = np.Client()
# print client.lampie
# print np.coordinator, client
# assert client == np.coordinator
#
# client2 = np.Client()
# print client.lampie
# print np.coordinator, client
# assert client != client2
#
#
# server = np.Server()
# print server.lampie
# print server, np.coordinator
# assert server != client


# # Picklability
# a = np.array([1, 2])
# print client.lampie
# b = np.array([1, 2])
# print client.lampie
# c = a + b
# print client.lampie
# s = client.dumps()
# print s
# t = client.loads(s)
# print client.lampie


# # Server Functionality
# server = np.Server()
# a = np.array([3.])
# print "a", a
# b = np.array([1.5])
# print "b", b
# c = a + b
# print c
# c = a - b
# print c
# c = a * b
# print c
# c = a / b
# print c
#
# a = 3
# print "a", a
# b = np.array([1.5])
# print "b", b
# c = a + b
# print c
# c = a - b
# print c
# c = a * b
# print c
# c = a / b
# print c
#
#
# a = np.array([3.])
# print "a", a
# b = 1.5
# print "b", b
# c = a + b
# print c
# c = a - b
# print c
# c = a * b
# print c
# c = a / b
# print c

# Client Functionality
client = Client(delay=False)
a = np.array([3.])
print "a", a
b = np.array([1.5])
print "b", b
with delay():
    c = a + b
    print c
print c

# # Delay Definition
# client = np.Client()
# print client.delay
# a = np.array([1])
# b = np.array([2])
# c = a + b
# with np.delay():
#     d = a - b
#     print client.delay
#     print d
# print d

# # File operation
# import h5py
# import numpy
# with h5py.File("tmp.hdf5", "w") as f:
#     a = numpy.random.random(size=(100, 100))
#     b = numpy.random.random(size=(100, 100))
#     f.create_dataset('a', data=a)
#     f.create_dataset('b', data=b)
#
# with h5py.File("tmp.hdf5", "r") as f:
#     a = f.get("a")
#     b = f.get("b")
#     na = np.array(numpy.array(a))
#     nb = np.array(numpy.array(b))
#     with np.delay():
#         nc = na + nb
#         print nc
#     print nc

# Client Functionality
