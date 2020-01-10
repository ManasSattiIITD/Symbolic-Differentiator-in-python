class expr:

	def __init__(self,S,Nd = None):
		if (Nd):
			self.expr = Nd
		else:
			(e,n) = self.parse(S)
			self.expr = e

	class Node:
		def __init__(self,d):
			self.left = None
			self.right = None
			self.data = d
		
		def toString(self):
			if (self.left and self.right):
				left = self.left.toString()
				right = self.right.toString()
				opr = self.data
				return "(" + left + " " + opr + " " + right + ")"
			else:
				return self.data

	def prettyprint(self):
		s = self.expr.toString()
		print(s)
		

	def parse(self,S):
		l = len(S)
		if (S[0] == "("):
			(left,n) =  self.parse(S[1:l-2])
			opr = S[n+1]
			(right,m) = self.parse(S[n+2:l-1])
			expr = self.Node(opr)
			expr.left = left
			expr.right = right
			return (expr,n+m+3)
		elif S[0].isdigit():
			i = 0
			while ((i < l) and (S[i].isdigit() or (S[i] == "."))):
				i = i+1
			num = S[0:i]
			expr = self.Node(num)
			return (expr,i)
		elif S[0].isalpha():
			i = 0
			while ((i < l) and S[i].isalpha()):
				i = i+1
			var = S[0:i]
			expr = self.Node(var)
			return (expr,i)
		else:
			return Exception("Invalid input")

	def constant(self):
		if self.expr.data[0].isdigit():
			return True
		else:
			return False

	def variable(self):
		if self.expr.data[0].isalpha():
			return True
		else:
			return False

	def samevariable(self,x):
		if (self.expr.data == x):
			return True
		else:
			return False

	def sum(self):
		if (self.expr.data == '+'):
			return True
		else:
			return False

	def addend(self):
		left = self.expr.left
		return expr("",left)

	def augend(self):
		right = self.expr.right
		return expr("",right)

	def makesum(self,e1,e2):
		e = self.Node("+")	

		#Original
		#e.left = e1
		#e.right = e2

		#Modified
		e.left = e1.expr
		e.right = e2.expr
		return expr("",e)

	def deriv(self,x):
		if self.constant():
			return expr("0.0")
		if self.variable():
			if self.samevariable(x):
				return expr("1.0")
			else:
				return expr("0.0")
		elif self.sum():
				e1 = self.addend()
				e2 = self.augend()
				return self.makesum(e1.deriv(x),e2.deriv(x))
		else:
			raise Exception("DontKnowWhatToDo!")
				



# a = input("Enter an expression:")
# e = expr(a)
# # print(e.expr.data,e.expr.left,e.expr.right)
# e.prettyprint()
# f = e.deriv('x')
# f.prettyprint()
# print(str(float("2.4")-1))
# print("a" > "A")
# print(("a" <= "2" <= "z") or ("A" <= "2" <= "Z") )