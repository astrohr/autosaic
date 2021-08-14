import requests
from bs4 import BeautifulSoup
import numpy as np

def linkInput():
    print("Paste the offsets link")
    return str(input())

def infoInput():
    print("Paste the object info")
    return str(input())

def compute(arr, info):
    date = info[0:15]
    ra = info[18:28]
    dec = info[29:38]
    spd = info[54:58]
    pa = info[60:65]

    cfields = np.array(["0 0"])
    sfields = np.array([0])
    for x in range(arr.size // 2):
        xsize = arr[x*2]
        ysize = arr[x*2+1]
        #print(str(xsize) + " " + str(ysize))
        if np.abs(xsize) < 1100 and np.abs(ysize) < 1100:
            sfields[0] += 1
        else:
            #print(str(xsize) + " " + str(ysize))
            yf = int(np.abs(ysize) // 1100)
            if ysize < 0:
                yf *= -1
            xf = int(np.abs(xsize) // 1100)
            if xsize < 0:
                xf *= -1
            c = str(xf) + " " + str(yf)
            confirm = False
            for i in range(cfields.size):
                if cfields[i] == c:
                    confirm = True
                    sfields += 1
                    break
            if confirm == False:
                cfields = np.append(cfields, str(xf) + " " + str(yf))
                sfields = np.append(sfields, int(1))

    #file1 = open("MyFile.txt","w")
    for i in range(sfields.size):
        dims = cfields[i].split(" ")
        
        rs = float(ra[6:10])
        rm = int(ra[3:5])
        rh = int(ra[0:2])
        rw = rh * 3600 + rm * 60 + rs + (2200 * int(dims[0]) / 15)
        rh = rw // 3600
        rw = rw % 3600
        rm = rw // 60
        rw = rw % 60
        rs = round(rw,1)
        newra = str(int(rh)) + " " + str(int(rm)) + " " + str(rs)

        ds = float(dec[7:9])
        dm = int(dec[4:6])
        dh = int(dec[0:3])
        dw = dh * 3600 + dm * 60 + ds + 2200 * int(dims[0])
        dh = dw // 3600
        dw = dw % 3600
        dm = dw // 60
        dw = dw % 60
        ds = round(dw,1)
        if dh < 0:
            newdec = str(int(dh)) + " " + str(int(dm)) + " " + str(int(ds))
        else:
            newdec = "+" + str(int(dh)) + " " + str(int(dm)) + " " + str(int(ds))
        scp = info[0:18] + newra + " " + newdec + info[38:]
        print("hits:" + str(sfields[i]))
        print(scp)
    #file1.close()
                

def main():
    lynk = '0'
    while lynk != '':
        info = infoInput()
        soup = BeautifulSoup(requests.get(linkInput()).content, "html.parser")
        table = soup.find("pre").contents
        arr = np.array([])
        for row in table:
            try:
                if str(row)[1] != 'N':
                    st = str(row)[1:20]
                else:
                    st = str(row)[12:31]
                st.strip(" ")
                if st[0] != "a":
                    spts = st.split(" ")
                    for spt in spts:
                        if str(spt) != '':
                            if str(spt[0]) == "-" or str(spt[0]) == "+":
                                arr = np.append(arr, int(spt))
                           
            except:
                break
        compute(arr, info)
        
if __name__ == "__main__":
    main()

