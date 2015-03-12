import plynet

#DICT TO OBJ
res=plynet.dict2obj(dict(a=1,b=2))
print res.a

res2=plynet.copyObject(res)

print plynet.BASEDIR

print plynet.conf.MODULE_NAME
print plynet.numeric.conf.MODULE_NAME
