import os
import inspect
import subprocess
import pexpect
import re
import sys

def runProcess(exe, LambdaName):    
    print("Started runProcess")
    try:
        child = pexpect.spawn(exe,cwd=LambdaName,timeout=300,logfile=sys.stdout,encoding='utf-8')
        child.expect ('Serverless: Would you like to enable this? (Y/n)')
        child.sendline ("n\n")
    except pexpect.EOF:
        # op = child.before.decode('ascii')
        op = child.before
        print("EOF ",op)
        ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
        l = [] 
        for x in op.split("\n"):
            s = ansi_escape.sub('', x).strip()
            if(len(s)>0):
                l.append(s)

        print(l)

        error = "Serverless Error ----------------------------------------"
        success = 'endpoints:'
        if(error in l):
            return False,l[l.index(error)+1]
        elif(success in l):
            return True, l[l.index(success)+1].split()[2]
        else:
            return False, "Unknown Error"

        
    except pexpect.TIMEOUT:
        print("TIMEOUT",child.before.decode('ascii'))
        return False, "Timeout Occured"
    except Exception as e:
        print(e,child.before.decode('ascii'))
        return False, "Exception Occured"
    
    return False, "Lambda creation ended"
    

def deploy(f, requirements, LambdaName, region="", access_key="", secret_access_key="", session_token=""):

    stream = os.popen("mkdir {0} && cd {0} && npm init -f && npm install --save-dev serverless-wsgi serverless-python-requirements".format(LambdaName))
    output = stream.read()
    print(output)

    obj=open("temp.py","w")
    obj.write(f)
    obj.close()
    temp=__import__("temp")

    func_obj = None

    for _,k in inspect.getmembers(temp):
        # print(type(k))
        if inspect.isfunction(k):
            func_obj = k
        # else:
        #     print("Problem in src string")

    params=list(inspect.signature(func_obj).parameters)
    print(params)

    route = '@app.route("/")'

    path = "/"

    for p in params:
        if len(path)==1:
            path += "<"+p+">"
        else:
            path += "/"+"<"+p+">"

    route = route.replace("/",path)

    f = route+"\n"+f

    stream = os.popen("cp app.py {0}/app.py && cp requirements.txt {0}/requirements.txt && cp serverless.yml {0}/serverless.yml".format(LambdaName))
    output = stream.read()
    print(output)

    obj=open("{0}/app.py".format(LambdaName),"a")
    obj.write("\n\n"+f)
    obj.close()

    reqs = requirements.strip()
    obj=open("{0}/requirements.txt".format(LambdaName),"a")
    obj.write("\n"+reqs)
    obj.close()

    obj=open("/home/mehul/.aws/credentials","w")
    obj.write("[default]\nregion={0}\naws_access_key_id={1}\naws_secret_access_key={2}\naws_session_token={3}".format(region,access_key,secret_access_key,session_token))
    obj.close()

    
    correct, res = runProcess("serverless deploy --aws-profile default",LambdaName)
    return correct, res

# LambdaName = "my-app"
# f = """def hello(s,a,b):
#     return "Hello World! " + s + " " + a + " " + b 
#     """

# print(deploy(f, "requests\nflask_cors", LambdaName, "us-east-1", "ASIAXVBHKSIVMI7TG67E", "HgxslS4RJO8RbQ/H6SExWjQCB75peLhOJyyA85nr", "FwoGZXIvYXdzEOP//////////wEaDIK9vIzutv/NWY5iXiLGAVikiBacgJf21T2s45VFTJAc0Vidsps6uLlLCyKrIsak3Cl/5dH+q+3VRkYzzwxLUh1Rdj6pAVTrsNBthPzqnTx2ILW46xCDwTt7tkuoTwy1dlyUjXLrvqJXERzNmzadTdt8r1NjIQshkLI3X6i6IJkmOXb5+0sFt8EhLW4YAJPBGodADs6FHofPaPAFg9M+Kf91Q8jcKLrUAnrTObstdm27LtlKT/TzyVSOhggYYRmqSmMiQVOilIt37H0CsyrREDqMtbBPFCjdwviCBjItd/2FycZD395K0Cih66RoRMR/AeD/OFWiejaCe7uu7EPyPg05yOxXYhKXXnb2"))