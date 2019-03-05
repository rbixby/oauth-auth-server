alist = []
adict = {"client_id": "1", "client_secret": "secret"}
alist.append(adict)

for a in alist:
    print(type(a))
    print(a["client_id"])