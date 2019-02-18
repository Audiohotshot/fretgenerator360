# Audiohotshot Fret Generator
# This plugin is under Common Creative License
# February 2019

import adsk.core, adsk.fusion, adsk.cam, traceback


# Global list to keep all event handlers in scope.
# This is only needed with Python.
handlers = []

def drawSketch(scalehigh, scalelow, fretno, fretwidth, fretoffset, dots, radius):
    # DRAWING STARTS HERE
    # Get the root component of the active design.
    app = adsk.core.Application.get()
    design = app.activeProduct
    rootComp = design.rootComponent        
    # Create a new sketch on the xy plane.
    sketches = rootComp.sketches;                                           
    xyPlane = rootComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    
    
    yup = 0- fretwidth / 2
    ydown =  fretwidth / 2
    lines = sketch.sketchCurves.sketchLines;
    # draw scalelines high and low
    lines.addByTwoPoints(adsk.core.Point3D.create(0, yup, 0), adsk.core.Point3D.create(scalehigh, yup, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(0 - fretoffset, ydown, 0), adsk.core.Point3D.create(scalelow - fretoffset, ydown, 0))
    #draw tremolo position line  
    lines.addByTwoPoints(adsk.core.Point3D.create(scalehigh, yup, 0), adsk.core.Point3D.create(scalelow - fretoffset, ydown, 0))
    #draw center construction line
    xconstructionstart = (0 - fretoffset) / 2
    yconstructionstart = 0
    xconstructionend = ((scalehigh + (scalelow - fretoffset)) /2)
    yconstructionend = 0
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(xconstructionstart, yconstructionstart, 0), adsk.core.Point3D.create(xconstructionend, yconstructionend, 0))    
    line1.isConstruction = True
    
    # draw individual frets
    n = 0
    while True:
        #draw fretlines        
        distancehigh = scalehigh - (scalehigh / 2 ** (n/12))
        distancelow = scalelow - fretoffset - (scalelow / 2 ** (n/12)) 
        lines.addByTwoPoints(adsk.core.Point3D.create(distancehigh, yup, 0), adsk.core.Point3D.create(distancelow, ydown, 0))        
        #counter        
        n = n + 1 
        if n == fretno:
            break
        
    #draw dots
    a = [0,0,1,0,1,0,1,0,1,0,0, 2,0,0,1,0,1,0,1,0,1,0,0, 2,0,0,1,0,1,0,1,0,1,0,0,2]
    if dots == True: 
        n = 0
        while True:
            if n != 0:
                s = a[n-1]
                #calculate centre dot
                xcentrehigh = scalehigh - (scalehigh / 2 ** ((n-0.5)/12))
                xcentrelow = scalelow - fretoffset - (scalelow / 2 ** ((n-0.5)/12))
                xcentre = (xcentrehigh + xcentrelow) /2
                ycentre = 0
                if s == 1:
                    #draw dot
                    circles = sketch.sketchCurves.sketchCircles
                    circles.addByCenterRadius(adsk.core.Point3D.create(xcentre, ycentre, 0), radius)
                if s == 2:
                    #calculate x position dots
                    xdistance = xcentrehigh - xcentrelow
                    if xdistance != 0:
                        xcircletop= xcentrehigh - (1/3 * fretwidth) / (fretwidth/xdistance)
                        xcirclebottom = xcentrehigh - (2/3 * fretwidth) / (fretwidth/xdistance)
                    else:
                        xcircletop= xcentrehigh
                        xcirclebottom = xcentrehigh 
                    #calculate y position dots
                    ycircletop = (0 -fretwidth / 2) + (fretwidth *  (1/3))
                    ycirclebottom = (0 -fretwidth / 2) + (fretwidth * (2/3))  
                    #draw dots
                    circles = sketch.sketchCurves.sketchCircles
                    circles.addByCenterRadius(adsk.core.Point3D.create(xcircletop, ycircletop, 0), radius)
                    circles.addByCenterRadius(adsk.core.Point3D.create(xcirclebottom, ycirclebottom, 0), radius)  
            n = n + 1 
            if n == fretno:
                break
       
def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get the CommandDefinitions collection.
        cmdDefs = ui.commandDefinitions
        
        # Create a button command definition.
        buttonSample = cmdDefs.addButtonDefinition('MyButtonDefIdPython', 
                                                   'Fret Generator', 
                                                   'Sample button tooltip',
                                                   './Resources')
        
        # Connect to the command created event.
        sampleCommandCreated = SampleCommandCreatedEventHandler()
        buttonSample.commandCreated.add(sampleCommandCreated)
        handlers.append(sampleCommandCreated)

        # Get the ADD-INS panel in the model workspace. 
        addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        
        # Add the button to the bottom of the panel.
        addInsPanel.controls.addCommand(buttonSample)
        if context['IsApplicationStartup'] == False:    
            ui.messageBox('The "Fret Generator" command has been added\nto the ADDIN panel')
            
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        
def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        # Clean up the UI.
        cmdDef = ui.commandDefinitions.itemById('MyButtonDefIdPython')
        if cmdDef:
            cmdDef.deleteMe()
            
        addinsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cntrl = addinsPanel.controls.itemById('MyButtonDefIdPython')
        if cntrl:
            cntrl.deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))	

# Event handler for the inputChanged event.
class SampleCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface            
            eventArgs = adsk.core.InputChangedEventArgs.cast(args)
            
            # Check the value of the check box.
            changedInput = eventArgs.input
            if changedInput.id == 'slanted':
                inputs = eventArgs.firingEvent.sender.commandInputs
                targetInput = inputs.itemById('scalelow')
                targetInput2 = inputs.itemById('slantedcentre')
           
                # Change the visibility of the scale value input.
                if changedInput.value == False:
                    targetInput.isVisible = False
                    targetInput2.isVisible = False
                else:
                    targetInput.isVisible = True
                    targetInput2.isVisible = True
    
            # Check the value of the check box.
            if changedInput.id == 'drawdots':
                inputs = eventArgs.firingEvent.sender.commandInputs
                targetInput = inputs.itemById('dotsize')
                # Change the visibility of the scale value input.
                if changedInput.value == False:
                    targetInput.isVisible = False
                else:
                    targetInput.isVisible = True
                    
        except:
            if ui:
                ui.messageBox(('Input changed event failed: {}').format(traceback.format_exc()))  

# Event handler for the execute event.
class SampleCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):                
        # Code to react to the event.
        app = adsk.core.Application.get()
        ui  = app.userInterface
        #ui.messageBox('In command execute event handler.')                          
        try:
            command = args.firingEvent.sender
            ui.messageBox(('command: {} executed successfully').format(command.parentCommandDefinition.id))
        except:
            if ui:
                ui.messageBox(('command executed failed: {}').format(traceback.format_exc()))
                
# Event handler for the commandCreated event.
class SampleCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:        
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            app = adsk.core.Application.get()
            ui  = app.userInterface     
            # Get the commandS
            cmd = eventArgs.command
    
            # Get the CommandInputs collection to create new command inputs.            
            inputs = cmd.commandInputs
    
            # Create the value input to get the scale. 
            inputs.addValueInput('scalehigh', 'Scale high', 'mm', adsk.core.ValueInput.createByReal(63.5))
                                              
            # Create a check box to get if it should be slanted  or not.
            inputs.addBoolValueInput('slanted', 'Slanted', True, '', False) 
                                                   
            # Create the value input to get the lower scale. 
            scaleLow = inputs.addValueInput('scalelow', 'Scale Low', 'mm', adsk.core.ValueInput.createByReal(68))
            scaleLow.isVisible = False
                                               
            # Create the value input to get the centre fret of the slanted scale. 
            slantedCentre = inputs.addValueInput('slantedcentre', 'Centre fret', '', adsk.core.ValueInput.createByReal(12)) 
            slantedCentre.isVisible = False                                          
                                                
            # Create the value input to get the amount of frets. 
            inputs.addValueInput('fretsno', 'Number of frets', '', adsk.core.ValueInput.createByReal(24))   
            #fretsNo = inputs.addIntegerSliderCommandInput('fretsno', 'Number of frets', 1, 36)
            
            # Create the value input to get the width of the board. 
            inputs.addValueInput('fretswidth', 'Width', 'mm', adsk.core.ValueInput.createByReal(5.5))   
                                                       
            # Create a check box to get if it should draw dots or not.
            inputs.addBoolValueInput('drawdots', 'Draw dots', True, '', False)  
    
            # Create the value input to get the dotsize
            dotsize = inputs.addValueInput('dotsize', 'Diameter', 'mm', adsk.core.ValueInput.createByReal(0.4))
            dotsize.isVisible = False  
                                        
            #errMessage = inputs.addTextBoxCommandInput('errMessage', '', '', 2, True)
            errMessage = inputs.addTextBoxCommandInput('errmessage', 'Text Box 1', '', 2, True)
            errMessage.isFullWidth = True                                    
            
            # Connect to the execute event.
            onExecute = SampleCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
    
            # Connect to the inputChanged event.
            onInputChanged = SampleCommandInputChangedHandler()
            cmd.inputChanged.add(onInputChanged)
            handlers.append(onInputChanged)
    
            # execute preview
            onExecutePreview = SampleCommandExecutePreviewHandler()
            cmd.executePreview.add(onExecutePreview)
            handlers.append(onExecutePreview)
            
            # execute validation
            onValidateInputs = SampleCommandValidateInputsHandler()
            cmd.validateInputs.add(onValidateInputs)
            handlers.append(onValidateInputs)
        except:
            if ui:
                ui.messageBox('Failed CreatedEventHandler:\n{}'.format(traceback.format_exc()))	

# Event handler for the validateInputs event.
class SampleCommandValidateInputsHandler(adsk.core.ValidateInputsEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface     
            
            eventArgs = adsk.core.ValidateInputsEventArgs.cast(args)
            inputs = eventArgs.firingEvent.sender.commandInputs
            
            # Verify that the scale is greater than 0.1.
            inputarg = inputs.itemById('fretsno').value
                   
            if inputarg < 37 and inputarg > 0:
                eventArgs.areInputsValid = True
                return
            else:
                eventArgs.areInputsValid = False
                
            
            inputarg = inputs.itemById('slantedcentre').value
            if inputarg < 37 and inputarg > 0:
                eventArgs.areInputsValid = True
                return
            else:
                eventArgs.areInputsValid = False
                
        except:
            if ui:
                ui.messageBox('Failed ValidateInputsHandler:\n{}'.format(traceback.format_exc()))
                
# Event handler for the executePreview event.
class SampleCommandExecutePreviewHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui  = app.userInterface     
                    
            eventArgs = adsk.core.CommandEventArgs.cast(args)
    
            # Get the command
            cmd = eventArgs.command
    
            # Get the CommandInputs collection to create new command inputs.            
            inputs = cmd.commandInputs
            
            slanted = inputs.itemById('slanted').value
            if slanted == False:    
                scalehigh = inputs.itemById('scalehigh').value        
                scalelow = inputs.itemById('scalehigh').value
                fretoffset = 0
            else:
                scalehigh = inputs.itemById('scalehigh').value   
                scalelow = inputs.itemById('scalelow').value            
                slantedcentre = inputs.itemById('slantedcentre').value
                frethighoffset = scalehigh - (scalehigh / 2 ** ( slantedcentre /12))
                fretlowoffset = scalelow - (scalelow / 2 ** ( slantedcentre /12))
                fretoffset = fretlowoffset - frethighoffset
            
            fretno = inputs.itemById('fretsno').value + 1
            fretwidth = -(inputs.itemById('fretswidth').value)
            
            drawdots = inputs.itemById('drawdots').value
            if drawdots == False:           
                dots = False
            else:
                dots = True
              
            radius = inputs.itemById('dotsize').value /2
            
            drawSketch(scalehigh, scalelow, fretno, fretwidth, fretoffset, dots, radius)
            
            # Set the isValidResult property to use these results at the final result.
            # This will result in the execute event not being fired.
            eventArgs.isValidResult = True

        except:
            if ui:
                ui.messageBox('Failed ValidateInputsHandler:\n{}'.format(traceback.format_exc()))

