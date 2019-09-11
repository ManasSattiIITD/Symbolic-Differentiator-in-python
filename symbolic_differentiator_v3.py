import math

class Expr:

	known_funcs = ['-','log','cos','sin']

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
			
			elif (self.type=='func'):
				name = self.data
				x = self.x.toString() 
				return name + '(' + x + ')'

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
		elif S[0].isdigit() or (S[0]=='-' and S[1].isdigit()):
			i = 0
			if(S[0]=='-'):
				i+=1
			while ((i < l) and (S[i].isdigit() or (S[i] == '.'))):
				i = i+1
			num = S[0:i]
			expr = self.Node(num,'num')
			return (expr,i)
		elif S[0].isalpha() or S[0]=='-':
			i = 0
			while ((i < l) and S[i].isalpha()):
				i = i+1
			var = S[0:i]
			if var in self.known_funcs:
				expr  = self.Node(var,'func')
				(expr.x,j) = self.parse(S[i+1:l-1])
				return (expr,i+j+2)
			else:
				expr = self.Node(var,'var')
				return (expr,i)
		else:
			return Exception('Invalid input')

	def is_num(self):
		return self.expr.type=='num'

	def is_var(self):
		return self.expr.type=='var'

	def is_oper(self):
		return self.expr.type=='oper'

	def is_func(self):
		return self.expr.type=='func'

	def is_same_as(self,x):
		return self.expr.data == x

	def is_sum(self):
		return self.expr.data == '+'
	
	def is_difference(self):
		return self.expr.data == '-'

	def is_product(self):
	    return self.expr.data == '*'

	def is_power(self):
	    return self.expr.data == '^'
	
	def is_quotient(self):
	    return self.expr.data == '/'

	def is_negative(self):
		return self.expr.data == '-'

	def is_log(self):
		return self.expr.data == 'log'

	def is_sin(self):
		return self.expr.data == 'sin'

	def is_cos(self):
		return self.expr.data == 'cos'

	def left_expr(self):
		left = self.expr.left
		return Expr('',left)

	def right_expr(self):
		right = self.expr.right
		return Expr('',right)

	def x_expr(self):
		x = self.expr.x
		return Expr('',x)

	def operate(self,op,l,r):
		e = self.Node(op,'oper')	
		e.left = l.expr
		e.right = r.expr
		return Expr('',e)

	def make_func(self,name,x):
		e = self.Node(name,'func')
		e.x = x.expr
		return Expr('',e)
		
	def find_sum(self,l,r):
		if(l.is_num() and r.is_num()):
			val = str(l.expr.val+r.expr.val)
			return Expr(val)
		if(l.is_num()):
			if(l.expr.val==0):
				return r
	    
		if(r.is_num()):
			if(r.expr.val==0):
				return l
	
		return self.operate('+',l,r)

	def find_difference(self,l,r):
		if(l.is_num() and r.is_num()):
			val = str(l.expr.val-r.expr.val)
			return Expr(val)
		if(r.is_num()):
			if(r.expr.val==0):
				return l 
		if(l.is_num()):
			if(l.expr.val==0):
				return self.make_func('-',r)
	
		return self.operate('-',l,r)

	def find_product(self,l,r):
		if(l.is_num() and r.is_num()):
			val = str(l.expr.val*r.expr.val)
			return Expr(val)
		if(l.is_num()):
			if(l.expr.val==0):
				return Expr('0')
			if(l.expr.val==1):
				return r
		if(r.is_num()):
			if(r.expr.val==0):
				return Expr('0')
			if(r.expr.val==1):
				return l
		
		return self.operate('*',l,r)

	def find_quotient(self,l,r):
		if(l.is_num() and r.is_num()):
			val = str(l.expr.val/r.expr.val)
			return Expr(val)
		if(r.is_num()):
			if(r.expr.val==0):
				raise Exception('DivisionByZeroNotDefined')
			if(r.expr.val==1):
				return l
		if(r.is_num()):
			if(r.expr.val==0):
				return Expr('0')
				    
		return self.operate('/',l,r)

	def find_power(self,l,r):
		if(l.is_num() and r.is_num()):
			val = str(l.expr.val**r.expr.val)
			return Expr(val)
		if(r.is_num()):
			if(r.expr.val==0):
				return Expr('1')
			if(r.expr.val==1):
				return l
		if(l.is_num()):
			if(l.expr.val==0):
				return Expr('0')
			if(l.expr.val==1):
				return Expr('1')
	    
		return self.operate('^',l,r)

	def deriv(self,x):
		if self.is_num():
			return Expr('0')
		
		if self.is_var():
			if self.is_same_as(x):
				return Expr('1')
			else:
				return Expr('0')

		if self.is_oper():
			if self.is_sum():
				l = self.left_expr()
				r = self.right_expr()
				return self.find_sum(l.deriv(x),r.deriv(x))

			if self.is_difference():
				l = self.left_expr()
				r = self.right_expr()
				return self.find_difference(l.deriv(x),r.deriv(x))

			
			if self.is_product():
				l = self.left_expr()
				r = self.right_expr()
				p = self.find_product(l.deriv(x),r)
				q = self.find_product(l,r.deriv(x))
				return self.find_sum(p,q)

			if self.is_quotient():
				l = self.left_expr()
				r = self.right_expr()
				p = self.find_product(l.deriv(x),r)
				q = self.find_product(l,r.deriv(x))
				p = self.find_difference(p,q)
				q = self.find_power(r,Expr('2'))
				return self.find_quotient(p,q)
				
			
			if self.is_power():
				l = self.left_expr()
				r = self.right_expr()
				r1 = self.find_sum(r,Expr('-1'))
				p = self.find_power(l,r1)
				p = self.find_product(p,l.deriv(x))
				p = self.find_product(r,p)

				log = self.make_func('log',l)
				q = self.find_product(self,r.deriv(x))
				q = self.find_product(log,q)

				return self.find_sum(p,q)

		if self.is_func():
			if self.is_negative():
				return self.make_func('-',self.x_expr().deriv(x))
			if self.is_log():
				q = self.find_quotient(Expr('1'),self.x_expr())
				return self.find_product(q,self.x_expr().deriv(x))
			if self.is_sin():
				p = self.make_func('cos',self.x_expr())
				return self.find_product(p,self.x_expr().deriv(x))
			if self.is_cos():
				p = self.make_func('sin',self.x_expr())
				p = self.make_func('-',p)
				return self.find_product(p,self.x_expr().deriv(x))
		
		raise Exception('DontKnowWhatToDo!')
				


a=input("Enter an exression: ")
e = Expr(a)
e.prettyprint()
f = e.deriv('x')
f.prettyprint()

