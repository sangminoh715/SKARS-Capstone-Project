from pid import pid
inputs = [7, 6, 1, -2, -3, -2, -1, 1, 0.5, 0]
p = 0.3
i = 0.2
d = 0.05
dt = 0.17

test_pid = pid(p,i,d,10)
for x in inputs:
    print(x)
    print(test_pid.get_pid(x,dt))
    print("\r\n")

