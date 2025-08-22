import openvr, time, math, keyboard, ctypes

# CONFIG
SENS_X = 5
SENS_Y = 5
DEADZONE = 1.5
DT = 0.01
MAX_DELTA = 30

RECENTER_KEY = 'r'
TOGGLE_KEY = 'pause'
EXIT_KEY = 'end'  # touche Fin pour quitter

# Windows API setup
SendInput = ctypes.windll.user32.SendInput
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]

def send_mouse_move(dx, dy):
    inp = INPUT(type=0, mi=MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, None))
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def click_right_down():
    inp = INPUT(type=0, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_RIGHTDOWN, 0, None))
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def click_right_up():
    inp = INPUT(type=0, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_RIGHTUP, 0, None))
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

# INIT SteamVR
openvr.init(openvr.VRApplication_Background)
vrsys = openvr.VRSystem()

tracking_enabled = False
click_right = False
prev_yaw = prev_pitch = 0
offset_yaw = offset_pitch = 0
accum_dx = accum_dy = 0

print("🎮 BeamVR prêt ! Toggle: Pause | Recentre: R | Quitte: Numpad '/'")

try:
    while True:
        if keyboard.is_pressed(EXIT_KEY):
            break

        if keyboard.is_pressed(TOGGLE_KEY):
            tracking_enabled = not tracking_enabled
            if tracking_enabled:
                print("🟢 Tracking activé")
                click_right_down()
                click_right = True
            else:
                print("🔴 Tracking désactivé")
                click_right_up()
                click_right = False
            time.sleep(0.5)

        if not tracking_enabled:
            time.sleep(DT)
            continue

        poses = vrsys.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount
        )
        pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
        if not pose.bPoseIsValid:
            print("⚠️ Tracking perdu")
            time.sleep(0.1)
            continue

        m = pose.mDeviceToAbsoluteTracking
        yaw = math.degrees(math.atan2(-m[0][2], m[2][2]))
        pitch = math.degrees(math.atan2(m[1][2], math.hypot(m[1][0], m[1][1])))

        if keyboard.is_pressed(RECENTER_KEY):
            offset_yaw = yaw
            offset_pitch = pitch
            print("🔄 Recentrage")
            time.sleep(0.5)

        yaw -= offset_yaw
        pitch -= offset_pitch

        # INVERSION DU SENS ICI
        dx = (yaw - prev_yaw) * SENS_X
        dy = (pitch - prev_pitch) * SENS_Y

        dx = max(min(dx, MAX_DELTA), -MAX_DELTA)
        dy = max(min(dy, MAX_DELTA), -MAX_DELTA)

        accum_dx += dx
        accum_dy += dy

        if abs(accum_dx) > DEADZONE or abs(accum_dy) > DEADZONE:
            send_mouse_move(int(accum_dx), int(accum_dy))
            accum_dx = 0
            accum_dy = 0

        prev_yaw = yaw
        prev_pitch = pitch
        time.sleep(DT)

except KeyboardInterrupt:
    print("🛑 Interruption clavier")

finally:
    openvr.shutdown()
    if click_right:
        click_right_up()
    print("✅ Fermé proprement")
