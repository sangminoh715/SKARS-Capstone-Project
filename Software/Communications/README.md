EXPLANATION
1. The child drone's Pi runs "child_com.py", whereas the parent runs "parent_com.py".
2. Each Raspberry Pi (on the child and on parent) contains a local copy of either "parent_status" or "child_status".
3. The Pi updates the local _status file every time the drone transitions to a new state.
4. The Pi then pushes this local _status file to the CSIL server.
4. The Pi then pulls information from the other drone from CSIL.

NOTE: Below, if "manual user controlled" is Yes, it means that the user manually sets the drone's status to that particular code.

CHILD CODES (read by parent):

       Code       |                Action                 |              Meaning                 |  Manual user controlled?
        C1        |          Not ready for docking        |  No battery, radio controlled, etc   |  Yes - Radio control, Maintenance, etc.
        C2        |          Looking to dock              |  Waypoint navigation in operation    |  Yes - Activate child to find parent
        C3        |          Locked OpenMV vision         |  Locked AprilTag - descend with PID  |  No - AutoPilot
        C4        |          Landed on parent             |  Turn off motors                     |  No - turned off

PARENT CODES (read by child):

       Code       |                Action                 |              Meaning                 |  Manual user controlled?
        P1        |          Not ready for docking        |  No battery, radio controlled, etc   |  Yes - Radio control, Maintenance, switch replacement batteries, etc.
        P2        |          Ready to dock                |  Hovering steadily in place          |  Yes - Active stable hovering
        P3        |          Switching battery            |  Linear actuator moves               |  No - handled by Pi
        P4        |          Child Ready for takeoff      |  Actuator fully retracted            |  No - handled by Pi

Order of operation and respective codes:
1. Both drones grounded                 (C1, P1)
2. Parent gets RTK GPS lock             (C1, P1)
3. Fly parent to certain location       (C1, P1)
4. Hover parent in place                (C1, P2)
5. Enable child drone to find parent    (C2, P2)
6. Child OpenMV locks AprilTag vision   (C3, P2)
7. Child lands on parent                (C4, P2)
8. Parent switches battery              (C4, P3)
9. Parent retracts actuator for takeoff (C4, P4)
10. Child takes off                     (C1, P2)
11. Fly Child back to base              (C1, P2)
12. Fly Parent back to base             (C1, P1)
