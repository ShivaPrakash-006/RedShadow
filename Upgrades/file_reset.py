import pickle
f = open(r'Python/SchoolProject/Red Shadow/Upgrades/upgrades.dat','rb')
print(pickle.load(f))
f.close()
f = open(r'Python/SchoolProject/Red Shadow/Upgrades/upgrades.dat','wb')
s = {"Crystal":[[1, 1, 50, 300, 300, 250, 300, 0], [1, 1, 50, 300, 300, 250, 300, 0], [1, 1, 30, 450, 450, 450, 200, 0], [1, 1, 50, 300, 300, 250, 300, 0], 1], 
"ArrowHead":[[3, 1, 50, 300, 300, 250, 300, 0], [3, 1, 50, 300, 300, 250, 300, 0], [5, 3, 10, 600, 600, 600, 100, 5], [3, 1, 50, 300, 300, 250, 250, 0], 0], 
"Helix":[[3, 1, 50, 300, 300, 250, 300, 0], [3, 1, 50, 300, 300, 250, 300, 0], [7, 7, 5, 900, 900, 900, 25, 10], [3, 1, 50, 300, 300, 250, 250, 0], 0], 
"Coins":0, "Selected":"Crystal"}
pickle.dump(s,f)
f.close()
f = open(r'Python/SchoolProject/Red Shadow/Upgrades/upgrades.dat','rb')
print(pickle.load(f))
f.close()

