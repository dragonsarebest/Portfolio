import pymel.core as pm
import maya.cmds as cmds

global MyWindow
global MyLayout
global DEBUG
global OrientJointsYesNo
global createIKSpline
global curve
global joints
global rootJoint
global scaleJoints
DEBUG = True

def dist(list1, list2):
    x = list1[0]-list2[0]
    y = list1[1]-list2[1]
    z = list1[2]-list2[2]
    return (x**2 + y**2 + z**2) ** 0.5 

def MainBody():
    global OrientJointsYesNo, createIKSpline, joints, rootJoint, scaleJoints
    joints = pm.selected()
    rootJoint = joints[0]
    scaleJoints = []
    cmds.select(clear=True)
    
    if(createIKSpline):
        print("createIKSpline is: ", createIKSpline)
        pm.select(rootJoint)
        splineEffectorCurve = pm.ikHandle(startJoint = rootJoint, endEffector = joints[-1], solver = 'ikSplineSolver', ccv = True, scv = True, pcv = True, roc = True, tws = 'linear', snc = True)
        #print(spline)
        postCurve(splineEffectorCurve, joints, rootJoint, scaleJoints)
    else:
        print("Not making ik spline handle.... select the curve you want to use instead")
        CreationWindow = cmds.window(title = "Not making ik spline handle.... select the curve you want to use instead", width = 600)
        CreationWindowLayout = cmds.rowColumnLayout( numberOfColumns=1, columnAttach=(1, 'right', 0), columnWidth=[(1, 100), (2, 250)], adjustableColumn = True)
        LoadFromFile = pm.button(label = "Set curve", parent = CreationWindowLayout, command = lambda *args: setCurve(CreationWindow) , width = 200)
        pm.scriptJob(uid=[CreationWindow, lambda *args: OnWindowClose(CreationWindow)])
        cmds.showWindow(CreationWindow)
    
    
def setCurve(CreationWindow):
    global curve
    """
    #debugging... finding what node type obj is
    selected_items = cmds.ls(selection=True)
    selected_shapes = cmds.listRelatives(selected_items[0], shapes=True)
    for item in selected_shapes:
        print(pm.nodeType(item))
    """
    selected_obj = cmds.ls(selection=True)
    selected_stuff = pm.selected()
    returnsStuff = []
    for i in range(0, len(selected_obj)):
        item = selected_obj[i]
        #print(str(pm.nodeType(item)))
        if(str(pm.nodeType(item)) == "nurbsCurve"):
            returnsStuff.append(selected_stuff[i])
        else:
            #since selecting a curve is actually selecting its transform...
            selected_shapes = cmds.listRelatives(item, shapes=True)
            if(selected_shapes == None):
                continue
            for shape in selected_shapes:
                if(str(pm.nodeType(shape)) == "nurbsCurve"):
                    returnsStuff.append(selected_stuff[i])
    print("selected: ", returnsStuff)
    if(len(returnsStuff) == 0 or returnsStuff == None):
        print("Please select a single curve!")
        curve = None
    else:
        #print("got a curve: ", returnsStuff[0])
        curve = returnsStuff[0]
        cmds.deleteUI("%s" % CreationWindow)
    
def OnWindowClose(nameOfWindow):
    global curve
    if(curve == None):
        print("Canceling: no curve selected...")
    else:
        tempList = []
        tempList.append(curve)
        postCurve(tempList, joints, rootJoint, scaleJoints)

def postCurve(splineEffectorCurve, joints, rootJoint, scaleJoints):
    global MyWindow, createIKSpline
    
    if(OrientJointsYesNo):
        orientJoints(joints)
    
    cmds.select(clear=True)
    for i in range(0, len(joints)):
        cmds.select(clear=True)
        pm.select(joints[i])
        
        # this doesnt do anything atm
        continue
        newScaleJoint = pm.joint()
        scaleJoints.append(newScaleJoint)
        
    locationOfTopJoint = pm.joint(joints[-1], q = True, p = True, a = True)
    controller = pm.circle( normal = (0, 1, 0), center = locationOfTopJoint , radius = 10)
   
    #finalControlVertex = pm.getAttr( '%s.cv[-1]' % (splineEffectorCurve[-1]) ) #just gets location, not object
    curveCVs = cmds.ls('{0}.cv[:]'.format(splineEffectorCurve[-1]), fl = True) # Get all cvs from curve
    controlCluster = cmds.cluster(curveCVs[-1])
    
    #centers pivot for this nurb circle
    cmds.select(clear=True)
    pm.select(controller)
    pm.xform(centerPivots = True)
    #parents cluster to control curve
    pm.parent(controlCluster, controller)
    
    
    if(createIKSpline):
        #extra controls
        #put control on 1st non root bone
        for i in range(0, 1): #can be changed LATER for more controllers
            locationOfJoint = pm.joint(joints[i], q = True, p = True, a = True)
            #ControlVertexLocation = pm.getAttr( '%s.cv[%s]' % (splineEffectorCurve[-1], str(i)) )
            controlCluster2 = cmds.cluster(curveCVs[i])
            #clusterLocation = pm.xform(controlCluster2, q = True, t = True, ws = True)
            controller2 = pm.circle( normal = (0, 1, 0), center = locationOfJoint , radius = 10)

            cmds.select(clear=True)
            pm.select(controller2)
            pm.xform(centerPivots = True)

            pm.parent(controlCluster2, controller2)
            #extra controls
        
    cmds.select(clear=True)
    pm.select(controller)
    controller = controller[0]
    #print(controller)
    
    controller.addAttr("Main_Stretch", attributeType = "float", keyable = True, defaultValue = 1.0)
    
    controller.addAttr("InitalArclenth", attributeType = "float", keyable = False, hidden = True)
    controller.addAttr("CurrentArclenth", attributeType = "float", keyable = False, hidden = True)
    
    controller.addAttr("LengthModifier", attributeType = "float", keyable = True, defaultValue = 1.0, minValue = 0.01, maxValue = 2.0)
    controller.addAttr("ParentDriver", attributeType = "float", keyable = True, defaultValue = 1.0)
    
    lengthOfCurve = pm.arclen(splineEffectorCurve[-1])
    pm.setAttr("%s.%s" % (controller, "InitalArclenth"), lengthOfCurve)
    
    for i in range(1, len(joints)):
        currentBone = joints[i]
        parentBone = joints[i-1]
        
        nameOfAttribute = "initalBoneDistance_"+str(i)
        bonePos = cmds.xform('%s' % currentBone, q = True, ws = True, rp = True)
        oldBonePos = cmds.xform('%s' % parentBone, q = True, ws = True, rp = True)
        
        distance = dist(oldBonePos, bonePos)
        
        positionAsPercentageofArcLen = distance
        controller.addAttr(nameOfAttribute, attributeType = "float", keyable = False, hidden = False)
        pm.setAttr("%s.%s" % (controller, nameOfAttribute), positionAsPercentageofArcLen)
    
    startOfCurve = splineEffectorCurve[-1].getShape().getCV(0)
    splineEffectorCurve[-1].setPivots(startOfCurve)
    #sets pivot to first control vertex
    
    #connect up everything!
    
    #connect the arclength of the curve to the main_stretch
    percentLength = cmds.shadingNode('multiplyDivide', asUtility=True, name='percentLength')
    pm.setAttr("%s.%s" % (percentLength, "operation"), 2)
    
    curveInfoNode = pm.arclen(splineEffectorCurve[-1], ch = True)
    
    #pm.connectAttr("%s.%s" % (curveInfoNode, "arcLength"), "%s.%s" % (controller, "CurrentArclenth"))
    
    pm.connectAttr("%s.%s" % (curveInfoNode, "arcLength"), "%s.%s" % (percentLength, "input1X"))
    pm.connectAttr("%s.%s" % (controller, "InitalArclenth"), "%s.%s" % (percentLength, "input2X"))
    
    LengthModifierNode = cmds.shadingNode('multiplyDivide', asUtility=True, name='LengthModifierNode')
    pm.connectAttr("%s.%s" % (controller, "LengthModifier"), "%s.%s" % (LengthModifierNode, "input1X"))
    pm.connectAttr("%s.%s" % (percentLength, "outputX"), "%s.%s" % (LengthModifierNode, "input2X"))
    
    parentModifierNode = cmds.shadingNode('multiplyDivide', asUtility=True, name='parentModifierNode')
    pm.connectAttr("%s.%s" % (LengthModifierNode, "outputX"), "%s.%s" % (parentModifierNode, "input1X"))
    pm.connectAttr("%s.%s" % (controller, "ParentDriver"), "%s.%s" % (parentModifierNode, "input2X"))
    
    pm.connectAttr("%s.%s" % (parentModifierNode, "outputX"), "%s.%s" % (controller, "Main_Stretch"))
    
    #pm.connectAttr("%s.%s" % (LengthModifierNode, "outputX"), "%s.%s" % (controller, "Main_Stretch"))
    
    #pm.connectAttr("%s.%s" % (percentLength, "outputX"), "%s.%s" % (controller, "Main_Stretch"))
    
    parentJ = None
    for i in range(0, len(joints)):
        j = joints[i]
        #jscale = scaleJoints[i]
        """
        #new distance length from parent = jBoneInitalParentBoneDistance * Main_stretch
        #direction = jBoneParentLocation - jBoneLocation (normalized)
        #jBoneTranslateX = jParentBoneLocation + new%oflengthAlongCurve * direction
        if(i != 0):
            #since we dont want to move the root bone
            
            #expressionString = "%s.translateX = %s.translateX + (%s.initalBoneDistance_%s * %s.Main_Stretch);" % (j, parentJ, controller, str(i), controller)
            expressionString = "%s.translateX = (%s.initalBoneDistance_%s * %s.Main_Stretch);" % (j, controller, str(i), controller)
            print("DEBUG:\n %s" % expressionString)
            #expressionString = "%s.translateX = %s.translateX + (%s.initalBoneDistance_%s * %s.Main_Stretch)*((%s.translateX-%s.translateX)/())" % (j, parentJ, controller, str(i), controller, j, parentJ)
            pm.expression(s = expressionString)
        
        parentJ = j
        """
        #works.... but not if what's being scaled has other limbs!
        
        pm.connectAttr("%s.%s" % (controller, "Main_Stretch"), "%s.%s" % (j, "scaleX"))
        
        multiplyDivideName = cmds.shadingNode('multiplyDivide', asUtility=True, name='InverseScale')
        pm.setAttr("%s.%s" % (multiplyDivideName, "operation"), 3)
        #0 = None, 1 = Mul, 2 = Div, 3 = Pow ?
        
        pm.connectAttr("%s.%s" % (controller, "Main_Stretch"), "%s.%s" % (multiplyDivideName, "input1X"))
        pm.connectAttr("%s.%s" % (controller, "Main_Stretch"), "%s.%s" % (multiplyDivideName, "input1Y"))
        pm.setAttr("%s.%s" % (multiplyDivideName, "input2X"), -0.5)
        pm.setAttr("%s.%s" % (multiplyDivideName, "input2Y"), -0.5)
        
        pm.connectAttr("%s.%s" % (multiplyDivideName, "outputX"), "%s.%s" % (j, "scaleY"))
        pm.connectAttr("%s.%s" % (multiplyDivideName, "outputY"), "%s.%s" % (j, "scaleZ"))
        
    cmds.select(clear=True)
    pm.select(controller)
    cmds.deleteUI("%s" % MyWindow)
    
def orientJoints(joints):
    pm.joint(joints[0], e = True, oj = "xyz", sao = "xup", ch = True, zso = True)
    locationOfTopJoint = pm.joint(joints[-1], q = True, p = True, a = True)
    locationOfSecondToTopJoint = pm.joint(joints[-2], q = True, p = True, a = True)
    #print("locationOfTopJoint: ", locationOfTopJoint)
    #print("locationOfSecondToTopJoint: ", locationOfSecondToTopJoint)
    distanceBetween = dist(locationOfTopJoint, locationOfSecondToTopJoint)
    forwardDir = []
    forwardDir.append(locationOfTopJoint[0] - locationOfSecondToTopJoint[0])
    forwardDir[0]/=distanceBetween
    forwardDir.append(locationOfTopJoint[1] - locationOfSecondToTopJoint[1])
    forwardDir[1]/=distanceBetween
    forwardDir.append(locationOfTopJoint[2] - locationOfSecondToTopJoint[2])
    forwardDir[2]/=distanceBetween
    #print("forwardDir:", forwardDir)

    newPos = []
    newPos.append(locationOfTopJoint[0] + forwardDir[0]*100)
    newPos.append(locationOfTopJoint[1] + forwardDir[1]*100)
    newPos.append(locationOfTopJoint[2] + forwardDir[2]*100)
    #print("new pos: ", newPos)

    cmds.select(clear=True)
    tempJoint = cmds.joint(p = newPos)
    #create a joint directly above the last joint
    #print("created a new joint")
    cmds.parent(tempJoint, "%s" % joints[-1])

    pm.joint(joints[0], e = True, oj = "xyz", sao = "xup", ch = True, zso = True)
    pm.delete(tempJoint)

def setOrient(value):
    global OrientJointsYesNo
    OrientJointsYesNo = value
    
def setIkSpline(value):
    global createIKSpline
    createIKSpline = value
    
def StartingWindow():
    global MyWindow, MyLayout, createIKSpline, OrientJointsYesNo
    
    MyWindow = cmds.window(title = "Squash&Stretch Tool", width = 400)
    MyLayout = pm.columnLayout( adjustableColumn = True , numberOfPopupMenus = 1)
    createIKSpline = True
    OrientJointsYesNo = False
    
    OrientJoints = pm.checkBox(label = "Orient Joints (might mess up the skeleton - so be careful)", onCommand = setOrient, offCommand = setOrient, value = OrientJointsYesNo)
    CreateIKSplineHandle = pm.checkBox(label = "Create IKSplineHandle (if no you will be prompted to choose an existing nurb curve)", onCommand = setIkSpline, offCommand = setIkSpline, value = createIKSpline)
    CreateSliderButton = pm.button(label = "Use These Joints", parent = MyLayout, width = 200)

    CreateSliderButton.setCommand("MainBody()")
    
    
    cmds.showWindow(MyWindow)


StartingWindow()
