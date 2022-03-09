import os
import time
from tkinter import *

import cv2
import psutil
import pyautogui
import ddddocr
import pyperclip
from matplotlib import pyplot as plt

def set_confirmed():
    cmd_set=[[2,"wx.png"],[1,"login.png"],[1,"xcx.png"],[1,"ehall.png"],[1,"enter.png"],[1,"pafd.png"],[1,"u.png"],[5,1],[6,-360],[1,"cmp_in.png"],[6,-900],[1,"lct.png"],[6,-3500],[1,"submit.png"],[1,"ok.png"],[4,"code.png"],[1,"confirm.png"]]    
    pids_set=psutil.pids()
    for pid in pids_set:
        #print(pid,psutil.Process(pid).name())
        if psutil.Process(pid).name() == "WeChat.exe":
            del cmd_set[1]
            break
    return cmd_set

def mouseClick(clicktimes,LorR,img,rpt_t=1):
    i=1
    js=0
    while True:
        #location = pyautogui.locateCenterOnScreen(img,confidence=0.9)
        location=idfy_by_chars(img)
        if location is not None:
            #pyautogui.click(location.x,location.y,clicks=clicktimes,button=LorR)
            pyautogui.click(location[0],location[1],clicks=clicktimes,button=LorR)
            i+=1
            print("Click success")
            if rpt_t>0:
                if i>rpt_t:
                    break
        else:
            if not js:
                print("No target! Retrying...")
            js+=1
            if js==50:
                print('Fail to click over 5 seconds, please check if there is a problem...')
        time.sleep(0.1)
        
def pafd():
    cmd_set=set_confirmed()

    for i in range(len(cmd_set)):
        cmd=cmd_set[i]
        print(cmd)
        if cmd[0]==1 or cmd[0]==2:
            img=cmd[1]
            mouseClick(cmd[0],"left",os.path.dirname(__file__)+'\\Photos\\'+img)
            if cmd[0]==1:
                print("Single Click",img)
            else:
                print("Double Click",img)
        elif cmd[0]==3:
            img=cmd[1]
            mouseClick(1,"right",os.path.dirname(__file__)+'\\Photos\\'+img)
            print("Right Click",img)   
            
        elif cmd[0]==4:
            img=pyautogui.screenshot(region=[887,435,146,48])
            img.save('cache.png')
            with open('cache.png','rb') as f:
                img_bytes = f.read()
            ocr=ddddocr.DdddOcr()
            res=ocr.classification(img_bytes)
            pyperclip.copy(res)
            mouseClick(1,"left",os.path.dirname(__file__)+'\\Photos\\'+cmd[1])
            pyautogui.hotkey('ctrl','v')
            print('input',res)
            
        elif cmd[0]==5:
            time.sleep(cmd[1])
            print("Wait for %.2f seconds"%(cmd[1]))
        elif cmd[0]==6:
            pyautogui.scroll(cmd[1],x=1000,y=500)
            print("Scroll %d"%cmd[1])

def idfy_by_chars(img_path,resize=0):
    img=cv2.imread(img_path)
    pyautogui.screenshot().save("Screenshot.png")
    dsp=cv2.imread("Screenshot.png")
    if resize:
        img=cv2.resize(img,None,fx=2,fy=2)
        dsp=cv2.resize(dsp,None,fx=2,fy=2)
    
    gray1=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray2=cv2.cvtColor(dsp, cv2.COLOR_BGR2GRAY)
    
    sift=cv2.xfeatures2d.SIFT_create()
    kp1,des1 = sift.detectAndCompute(gray1, None)
    kp2,des2 = sift.detectAndCompute(gray2, None)
    
    '''
    for kp in kp1:
        print(kp.pt)
    '''
    
    #bf = cv2.BFMatcher(normType=cv2.NORM_L1, crossCheck=True)
    #matches = bf.match(des1,des2)
    #matches = sorted(matches, key=lambda x:x.distance)

    if len(kp1)<5:

        pos=idfy_by_chars(img_path,1)
        
        if not pos==None:
            return (int(pos[0]/2),int(pos[1]/2))
        else:
            return pos
        
    else:
        matches = cv2.BFMatcher().knnMatch(des1,des2,k=2)

        for m,n in matches:
            print(m.distance,"|",n.distance)

        good=[m for m,n in matches if (m.distance<0.7*n.distance) or (m.distance<100)]
        print(len(good),len(kp1))
        '''
        for m in good:
            print(m.trainIdx,m.queryIdx,m.imgIdx)
        '''
        src_pts=[tuple([int(pos) for pos in kp1[m.queryIdx].pt]) for m in good]
        #print(src_pts)
        dst_pts=[tuple([int(pos) for pos in kp2[m.trainIdx].pt]) for m in good]
        #print(dst_pts)

        if len(good)>0.5*len(kp1):
            return dst_pts[0]
        else:
            return None

    '''
    #preview=cv2.drawMatches(img1=img,keypoints1=kp1,img2=dsp,keypoints2=kp2,matches1to2=matches,outImg=dsp,flags=2)
    good=[[m] for m in good]
    preview=cv2.drawMatchesKnn(img,kp1,dsp,kp2,good,None)
    plt.imshow(preview)
    plt.show()
    '''

'''
class Ui(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master.title('pafd')
        self.master.geometry('1080x720')
        self.createWidgets()

    def createWidgets(self):
        self.top=self.winfo_toplevel()
        self.txt=Text(self.top)
        self.txt.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)

    def refresh(self,text):
        self.txt.insert(1.0,text+'\n')

class pafd(Ui):
    def __init__(self,master=None):
        Ui.__init__(self,master)
        self.run(self)

    def run(self,event=None):
        cmd_set=set_confirmed()

        for i in range(len(cmd_set)):
            cmd=cmd_set[i]
            print(cmd)
            if cmd[0]==1 or cmd[0]==2:
                img=cmd[1]
                print(os.path.dirname(__file__)+'\\Photos\\'+img)
                self.mouseClick(cmd[0],"left",os.path.dirname(__file__)+'\\Photos\\'+img)
                if cmd[0]==1:
                    self.refresh("Single Click"+img)
                else:
                    self.refresh("Double Click"+img)
            elif cmd[0]==3:
                img=cmd[1]
                self.mouseClick(1,"right",os.path.dirname(__file__)+'\\Photos\\'+img)
                self.refresh("Right Click",img)   
                
            elif cmd[0]==4:
                img=pyautogui.screenshot(region=[887,435,146,48])
                img.save('cache.png')
                with open('cache.png','rb') as f:
                    img_bytes = f.read()
                ocr=ddddocr.DdddOcr()
                res=ocr.classification(img_bytes)
                pyperclip.copy(res)
                self.mouseClick(1,"left",os.path.dirname(__file__)+'\\Photos\\'+cmd[1])
                pyautogui.hotkey('ctrl','v')
                self.refresh('input',res)
                
            elif cmd[0]==5:
                time.sleep(cmd[1])
                self.refresh("Wait for %.2f seconds"%(cmd[1]))
            elif cmd[0]==6:
                pyautogui.scroll(cmd[1],x=1000,y=500)
                self.refresh("Scroll %d"%cmd[1])

    def mouseClick(clicktimes,LorR,img,rpt_t=1):
        i=1
        js=0
        while True:
            location = pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clicktimes,button=LorR)
                i+=1
                self.refresh("Click success")
                if rpt_t>0:
                    if i>rpt_t:
                        break
            else:
                if not js:
                    self.refresh("No target! Retrying...")
                js+=1
                if js==50:
                    self.refresh('Fail to click over 5 seconds, please check if there is a problem...')
            time.sleep(0.1)
'''

if __name__=='__main__':
    
    pafd()
    '''
    top=Tk()
    pafd(top).mainloop()
    '''
