# -*- coding: utf-8 -*- 

import maya.cmds as mc
import maya.mel as mel
import random

class ShakeCamera:

    def MainMenu(self,*args):
        mc.window(t='ShakeCamera')
        mc.columnLayout(adj=True)
        mc.checkBoxGrp('axis', l='Shake Axis', ncb=3, la3=['X','Y','Z'])
        mc.intSliderGrp('shake', l='Max Shake', f=True, min=1, max=30)
        mc.intSliderGrp('interval',l='Frame interval', f=True, min=1, max=30)
        mc.button(l='Expression', c=self.expression)
        mc.button(l='Delete',c="mc.delete('ShakeCamera')")
        mc.showWindow()

    def expression(self,*args):
        #------------------------------------------------
        camcheck = mc.ls()
        cam = mc.select()
        xche = mc.checkBoxGrp('axis', q=True, v1=True)
        yche = mc.checkBoxGrp('axis', q=True, v2=True)
        zche = mc.checkBoxGrp('axis', q=True, v3=True)
        inter = mc.intSliderGrp('interval', q=True, v=True)
        inpshake = mc.intSliderGrp('shake', q=True, v=True)
        #-----------------------------------------------
        if 'ShakeCamera' in camcheck:
            mc.delete('ShakeCamera')
        if inter == 0 or inpshake == 0:
            print('ERROR : 0 cannot be selected.')
            return
        if xche == 0 and yche == 0 and zche == 0:
            print('ERROR : Please select at least one axis to shake.')
            return
        #-----------------------------------------------
        firstkey = mc.findKeyframe(cam,ts=True,w='first')
        lastkey = mc.findKeyframe(cam,ts=True,w='last')
        expkey = lastkey - firstkey
        startkey = firstkey + inter
        #----------------------------------------
        mc.animLayer('ShakeCamera',aso=True)
        mc.currentTime(firstkey)
        mc.setKeyframe(at='translate',t=firstkey)
        mel.eval('setKeyframe ShakeCamera.weight;')
        mc.currentTime(lastkey)
        mel.eval('setKeyframe ShakeCamera.weight;')
        mc.setKeyframe(at='translate',t=lastkey)
        mc.currentTime(startkey)
        mel.eval('setKeyframe ShakeCamera.weight;')
        #------------------------------------------
        for i in range(int(expkey)):
            if expkey <= startkey:
                break
            else:
                mc.currentTime(startkey)
                mc.animLayer('ShakeCamera', e=True, m=True, l=True)
                tx = mc.getAttr(cam,'.tx')
                ty = mc.getAttr(cam,'.ty')
                tz = mc.getAttr(cam,'.tz')
                mc.animLayer('ShakeCamera', e=True, m=False, l=False)
                intshakex = inpshake + tx
                intshakey = inpshake + ty
                intshakez = inpshake + tz
                rpshaX = random.uniform(tx,intshakex)
                rpshaY = random.uniform(ty,intshakey)
                rpshaZ = random.uniform(tz,intshakez)
                if xche == 1:
                    mc.setKeyframe(at='translateX',t=startkey,v=rpshaX)
                if yche == 1:
                    mc.setKeyframe(at='translateY',t=startkey,v=rpshaY)
                if zche == 1:
                    mc.setKeyframe(at='translateZ',t=startkey,v=rpshaZ)
                startkey = startkey + inter
                mc.currentTime(startkey)
                mc.animLayer('ShakeCamera', e=True, m=True, l=True)
                tx = mc.getAttr(cam,'.tx')
                ty = mc.getAttr(cam,'.ty')
                tz = mc.getAttr(cam,'.tz')
                mc.animLayer('ShakeCamera', e=True, m=False, l=False)
                minintshakex = -inpshake + tx
                minintshakey = -inpshake + ty
                minintshakez = -inpshake + tz
                rmshaX = random.uniform(minintshakex,tx)
                rmshaY = random.uniform(minintshakey,ty)
                rmshaZ = random.uniform(minintshakez,tz)
                if xche == 1:
                    mc.setKeyframe(at='translateX',t=startkey,v=rmshaX)
                if yche == 1:
                    mc.setKeyframe(at='translateY',t=startkey,v=rmshaY)
                if zche == 1:
                    mc.setKeyframe(at='translateZ',t=startkey,v=rmshaZ)
                startkey = startkey + inter
        #------------------------------------------

a = ShakeCamera()
a.MainMenu()