from bmob import Bmob

b = Bmob('ea71057d7956ef1d4d7fa5959ab550c2','b3e8b1012593f2ace272123ec25654ba')
user = b.login('heshaoyue','123456')

islogin = b.checkSession('98575e8482')
if islogin is None:
    print(b.getError())
else:
    print(islogin)