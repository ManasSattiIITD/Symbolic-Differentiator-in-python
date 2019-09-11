class EXPR:

	def __init__(self,S,Nd = None):
		if (Nd):
			self.expr = Nd
		else:
			(e,_) = self.parse(S)
			self.expr = e

	class Node:
		def __init__(self,d,t):
			self.type = t
			self.data = d
			if(self.type=='oper'):
				self.left = None
				self.right = None
			if(self.type=='num'):
				self.val = float(self.data)
			if(self.type=='func'):
				self.x  = None
		
		def toString(self):

			if (self.type=='oper'):
				left = self.left.toString()
				right = self.right.toString()
				opr = self.data
				return '(' + left + ' ' + opr + ' ' + right + ')'
			else:
				return self.data

	def prettyprint(self):
		s = self.expr.toString()
		print(s)
		

	def parse(self,S):
		l = len(S)
		if (S[0] == '('):
			(left,n) =  self.parse(S[1:l-2])
			opr = S[n+1]
			(right,m) = self.parse(S[n+2:l-1])
			expr = self.Node(opr,'oper')
			expr.left = left
			expr.right = right
			return (expr,n+m+3)
		elif S[0].isdigit():
			i = 0
			while ((i < l) and (S[i].isdigit() or (S[i] == '.'))):
				i = i+1
			num = S[0:i]
			expr = self.Node(num,'num')
			return (expr,i)
		elif S[0].isalpha():
			i = 0
			while ((i < l) and S[i].isalpha()):
				i = i+1
			var = S[0:i]
			expr = self.Node(var,'var')
			return (expr,i)
		else:
			return Exception('Invalid input')

	def isnumber(self):
		return self.expr.type=='num'

	def isvar(self):
		return self.expr.type=='var'

	def isoper(self):
		return self.expr.type=='oper'

	def isfunc(self):
		return self.expr.type=='func'

	def samevariable(self,x):
		return self.expr.data == x

	def issum(self):
		return self.expr.data == '+'
	
	def isdifference(self):
		return self.expr.data == '-'

	def isproduct(self):
	    return self.expr.data == '*'

	def ispower(self):
	    return self.expr.data == '^'
	
	def isquotient(self):
	    return self.expr.data == '/'

	def lp(self):
		left = self.expr.left
		return EXPR('',left)

	def rp(self):
		right = self.expr.right
		return EXPR('',right)

	def x_expr(self):
		x = self.expr.x
		return EXPR('',x)

	def opera(self,op,l,r):
		e = self.Node(op,'oper')	
		e.left = l.expr
		e.right = r.expr
		return EXPR('',e)


		
	def sum(self,l,r):
		if(l.isnumber() and r.isnumber()):
			val = str(l.expr.val+r.expr.val)
			return EXPR(val)
		if(l.isnumber()):
			if(l.expr.val==0):
				return r
	    
		if(r.isnumber()):
			if(r.expr.val==0):
				return l
	
		return self.opera('+',l,r)

	def difference(self,l,r):
		if(l.isnumber() and r.isnumber()):
			val = str(l.expr.val-r.expr.val)
			return EXPR(val)
		if(r.isnumber()):
			if(r.expr.val==0):
				return l 
		if(l.isnumber()):
			if(l.expr.val==0):
				return self.make_func('-',r)
	
		return self.opera('-',l,r)

	def product(self,l,r):
		if(l.isnumber() and r.isnumber()):
			val = str(l.expr.val*r.expr.val)
			return EXPR(val)
		if(l.isnumber()):
			if(l.expr.val==0):
				return EXPR('0')
			if(l.expr.val==1):
				return r
		if(r.isnumber()):
			if(r.expr.val==0):
				return EXPR('0')
			if(r.expr.val==1):
				return l
		
		return self.opera('*',l,r)

	def quotient(self,l,r):
		if(l.isnumber() and r.isnumber()):
			val = str(l.expr.val/r.expr.val)
			return EXPR(val)
		if(r.isnumber()):
			if(r.expr.val==0):
				raise Exception('DivisionByZeroNotDefined')
			if(r.expr.val==1):
				return l
		if(r.isnumber()):
			if(r.expr.val==0):
				return EXPR('0')
				    
		return self.opera('/',l,r)

	def power(self,l,r):
		if(l.isnumber() and r.isnumber()):
			val = str(l.expr.val**r.expr.val)
			return EXPR(val)
		if(r.isnumber()):
			if(r.expr.val==0):
				return EXPR('1')
			if(r.expr.val==1):
				return l
		if(l.isnumber()):
			if(l.expr.val==0):
				return EXPR('0')
			if(l.expr.val==1):
				return EXPR('1')
	    
		return self.opera('^',l,r)

	def derivative(self,x):
		if self.isnumber():
			return EXPR('0')
		
		if self.isvar():
			if self.samevariable(x):
				return EXPR('1')
			else:
				return EXPR('0')

		if self.isoper():
			if self.issum():
				l = self.lp()
				r = self.rp()
				return self.sum(l.derivative(x),r.derivative(x))

			if self.isdifference():
				l = self.lp()
				r = self.rp()
				return self.difference(l.derivative(x),r.derivative(x))

			
			if self.isproduct():
				l = self.lp()
				r = self.rp()
				p = self.product(l.derivative(x),r)
				q = self.product(l,r.derivative(x))
				return self.sum(p,q)

			if self.isquotient():
				l = self.lp()
				r = self.rp()
				p = self.product(l.derivative(x),r)
				q = self.product(l,r.derivative(x))
				p = self.difference(p,q)
				q = self.power(r,EXPR('2'))
				return self.quotient(p,q)
				
			
			if self.ispower():
				l = self.lp()
				r = self.rp()
				r1 = self.sum(r,EXPR('-1'))
				p = self.power(l,r1)
				p = self.product(p,l.derivative(x))
				p = self.product(r,p)
				q = self.product(self,r.derivative(x))
				q = self.product(log,q)
				return self.sum(p,q)
		
		raise Exception('DontKnowWhatToDo!')
				

a = input("Enter a expresion : ")
e = EXPR(a)
e.prettyprint()
f = e.derivative('x')
f.prettyprint()

((2*x)^2)
