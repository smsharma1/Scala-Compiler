import removejumps
filep = open("ThreeAddressCode.txt")
data = filep.readlines()
newf = open("taccopy.txt", "w")
newf.write(removejumps.removejumps(data))

