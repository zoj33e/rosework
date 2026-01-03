#SingleInstance Force
#NoEnv
SetBatchLines, -1
CoordMode, Pixel, Screen
CoordMode, Mouse, Screen

; global state
global macroOn := false
global moveState := "NONE"
global lastLowTime := 0
global REGEN_DELAY := 5000

F1::
macroOn := !macroOn

if (macroOn) {
    ToolTip, auto run on
    SetTimer, StaminaLoop, 1000
} else {
    ToolTip, auto run off
    SetTimer, StaminaLoop, Off
    StopMove()
    SetTimer, ClearTip, -800
}
return

ClearTip:
ToolTip
return

StaminaLoop:
currentTime := A_TickCount

if (IsStaminaLow()) {
    lastLowTime := currentTime

    if (moveState != "WALK") {
        ToolTip, stamina low, walking
        Walk()
        moveState := "WALK"
    }
}
else {
    ; stamina no longer red
    if (currentTime - lastLowTime >= REGEN_DELAY) {
        if (moveState != "RUN") {
            ToolTip, stamina regenerated
            Run()
            moveState := "RUN"
        }
    } else {
        ; still waiting for regen delay
        if (moveState != "WALK") {
            ToolTip, waiting stamina to regenerate
            Walk()
            moveState := "WALK"
        }
    }
}
return


IsStaminaLow() {
    PixelSearch, px, py
        , 1295, 910     
        , 1315, 925     
        , 0x661A16      
        , 25            
        , RGB
    return ErrorLevel = 0
}

Run() {
    Send, {w up}
    Sleep, 25
    Send, w
    Sleep, 40
    Send, {w down}
}

Walk() {
    Send, {w up}
    Sleep, 25
    Send, {w down}
}

StopMove() {
    Send, {w up}
}


F2::
macroOn := false
SetTimer, StaminaLoop, Off
StopMove()
ToolTip, Stop
SetTimer, ClearTip, -1000
return

F3::ExitApp