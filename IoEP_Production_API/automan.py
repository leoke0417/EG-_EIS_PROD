'''
Created on 2010/11/25
@author: panda.huang
'''
import sys
from automan.tool.parse_file import Parse_file
from automan.tool.execute_qa import Execute_qa
import automan.tool.error as error
  
if __name__ == '__main__':
    try:
        argv = sys.argv[1:]
        if len(argv) == 0:
            raise  error.noqafile()
        qa_list = Parse_file().search_file(argv[0])
        Execute_qa().execute_qa_list(argv[0],qa_list)
       
    except  error.noqafile:
        print ("no qa file")
    except error.notfindqafile:
        print ("not find qafile")
    except error.notfindinifile:
        print ("not find inifile")
    except error.notfindincludefile:
        print ("not find include file")

    #else:
    #    print "unhandle error!!!"