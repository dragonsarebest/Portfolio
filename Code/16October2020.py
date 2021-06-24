def eval(expression):
    expression = expression.replace(" ", "")

    #print("EXPFESSION: ", expression)
    
    if(expression[0] == "-"):
        #print("NEG: ", expression)
        val = -1 * eval(expression[1:])
        return val
    elif(expression[0].isnumeric()):
        if(len(expression) == 1):
            val = int(expression)
            #print(val)
            return val
        if(expression[1] == "-"):
            #print("normal sub", expression)
            val = int(expression[0]) - eval(expression[2:])
            #print(val)
            return val
        if(expression[1] == "+"):
            val = int(expression[0]) + eval(expression[2:])
            #print(val)
            return val
    else:
        #parenthesis
        firstParen = False
        index = 0
        numopen = 0
        for i in range(0, len(expression)):
            if(expression[i] == "("):
                numopen += 1
                if(firstParen == False):
                    index = i
                firstParen = True
            if(expression[i] == ")"):
                numopen -= 1
            if(numopen == 0 and firstParen):
                inside = eval(expression[index+1:i])
                #print("prestructured: ", expression[index+1:i])
                expression = expression[0:index] + str(inside) + expression[i+1:]
                #print("restructured: ", expression)
                return eval(expression)

print(eval('- (3 + ( 2 - 1 ) - 1)'))
#-3
print(eval('- (3 + ( 2 - 1 ) + 2 - 2 ) + 4 - 4 - ( - 2 ) - 2'))
# -4
print(eval('4 -( - 2 ) - 2'))
# 4

print(eval('4 -( - 2 )'))
# 6
