# expressions.py
from manim import *
from .utils import *


algebra_config = {
		"auto_parentheses": True,
		"multiplication_mode": "juxtapose",
		"division_mode": "fraction",
		"decimal_precision": 4,
		"always_color": {}
	}


# Main Class
class SmartExpression(MathTex):
	def __init__(self, parentheses=False, **kwargs):
		self.parentheses = parentheses
		if algebra_config["auto_parentheses"]:
			self.auto_parentheses()
		string = add_spaces_around_brackets(str(self))
		super().__init__(string, **kwargs)

	def __getitem__(self, key):
		if isinstance(key, str): # address of subexpressions, should return the glyphs corresponding to that subexpression
			return VGroup(*[self[0][g] for g in self.get_glyphs(key)])
		else: # preserve behavior of MathTex indexing
			return super().__getitem__(key)

	def get_all_addresses(self):
		# Returns the addresses of all subexpressions
		addresses = [""]
		for n in range(len(self.children)):
			for child_address in self.children[n].get_all_addresses():
				addresses.append(str(n)+child_address)
		return addresses
	
	def get_all_nonleaf_addresses(self):
		return sorted(list({a[:-1] for a in self.get_all_addresses() if a != ""}))
	
	def get_all_leaf_addresses(self):
		return sorted(list(set(self.get_all_addresses()) - set(self.get_all_nonleaf_addresses())))

	def get_subex(self, address_string):
		# Returns the SmartTex object corresponding to the subexpression at the given address.
		# Note that this is not a submobject of self! It is a different mobject probably not on screen,
		# it was just created to help create self.
		if address_string == "":
			return self
		elif int(address_string[0]) < len(self.children):
			return self.children[int(address_string[0])].get_subex(address_string[1:])
		else:
			raise IndexError(f"No subexpression of {self} at address {address_string} .")

	def is_identical_to(self, other):
		# Checks if they are equal as expressions. Implemented separately in leaves.
		# NOT the same as __eq__ which is used by Manim to check if two mobjects are identical
		# Different instances of the same expression are different mobjects
		return type(self) == type(other) and len(self.children) == len(other.children) \
			and all(self.children[i].is_identical_to(other.children[i]) for i in range(len(self.children)))

	def get_addresses_of_subex(self, subex):
		subex = Smarten(subex)
		addresses = []
		for ad in self.get_all_addresses():
			if self.get_subex(ad).is_identical_to(subex):
				addresses.append(ad)
		return addresses

	def get_glyphs_at_address(self, address):
		start = 0
		for n,a in enumerate(address):
			parent = self.get_subex(address[:n])
			if parent.parentheses:
				start += parent.paren_length()
			if isinstance(parent, SmartCombiner):
				for i in range(int(a)):
					sibling = parent.children[i]
					start += len(sibling)
					start += parent.symbol_glyph_length
			elif isinstance(parent, SmartNegative):
				start += 1
			elif isinstance(parent, SmartFunction):
				start += parent.symbol_glyph_length
			else:
				raise ValueError(f"Invalid parent type: {type(parent)}. n={n}, a={a}.")
		end = start + len(self.get_subex(address))
		return list(range(start, end))

	def get_left_paren_glyphs(self, address):
		subex = self.get_subex(address)
		if not subex.parentheses:
			return []
		subex_glyphs = self.get_glyphs_at_address(address)
		start = subex_glyphs[0]
		end = start + subex.paren_length()
		return list(range(start, end))

	def get_right_paren_glyphs(self, address):
		subex = self.get_subex(address)
		if not subex.parentheses:
			return []
		subex_glyphs = self.get_glyphs_at_address(address)
		end = subex_glyphs[-1]
		start = end - subex.paren_length()
		return list(range(start+1, end+1))
	
	def get_exp_glyphs_without_parentheses(self, address):
		subex = self.get_subex(address)
		subex_glyphs = self.get_glyphs_at_address(address)
		if not subex.parentheses:
			return subex_glyphs
		else:
			paren_length = subex.paren_length()
			return subex_glyphs[paren_length:-paren_length]
	
	def get_op_glyphs(self, address):
		subex = self.get_subex(address)
		if not isinstance(subex, SmartCombiner) or subex.symbol_glyph_length==0:
			return []
		subex_glyphs = self.get_glyphs_at_address(address)
		results = []
		turtle = subex_glyphs[0]
		if subex.parentheses:
			turtle += subex.paren_length()
		for child in subex.children[:-1]:
			turtle += len(child)
			results += list(range(turtle, turtle + subex.symbol_glyph_length))
			turtle += subex.symbol_glyph_length
		return results
	
	def get_glyphs(self, psuedoaddress):
		# Returns the list of glyph indices corresponding to the subexpression at the given address.
		# Can accept special characters at the end to trigger one of the special methods above.
		special_chars = "()_+-*/^"
		found_special_chars = [(i,c) for (i,c) in enumerate(psuedoaddress) if c in special_chars]
		if len(found_special_chars) == 0:
			return self.get_glyphs_at_address(psuedoaddress)
		else:
			address = psuedoaddress[:found_special_chars[0][0]]
			results = []
			for i,c in found_special_chars:
				if c == "(":
					results += self.get_left_paren_glyphs(address)
				elif c == ")":
					results += self.get_right_paren_glyphs(address)
				elif c == "_":
					results += self.get_exp_glyphs_without_parentheses(address)
				elif c in "+-*/^":
					results += self.get_op_glyphs(address)
			return sorted(set(results))

	def __len__(self):
		return len(self.submobjects[0].submobjects)

	def __neg__(self):
		return SmartNegative(self)

	def __add__(self, other):
		return SmartAdd(self, other)

	def __sub__(self, other):
		return SmartSub(self, other)

	def __mul__(self, other):
		return SmartMul(self, other)

	def __truediv__(self, other):
		return SmartDiv(self, other)

	def __pow__(self, other):
		return SmartPow(self, other)

	def __radd__(self, other):
		return SmartAdd(other, self)

	def __rsub__(self, other):
		return SmartSub(other, self)

	def __rmul__(self, other):
		return SmartMul(other, self)

	def __rtruediv__(self, other):
		return SmartDiv(other, self)

	def __rpow__(self, other):
		return SmartPow(other, self)

	def __iadd__(self, other):
		return self.__add__(other)

	def __isub__(self, other):
		return self.__sub__(other)

	def __imul__(self, other):
		return self.__mul__(other)

	def __itruediv__(self, other):
		return self.__truediv__(other)

	def __ipow__(self, other):
		return self.__pow__(other)

	def __matmul__(self, expression_dict):
		return self.substitute(expression_dict)

	def __and__(self, other):
		return SmartEquation(self, other)
	
	def __rand__(self, other):
		return SmartEquation(other, self)

	def is_negative(self):
		return False # catchall if not defined in subclasses

	def give_parentheses(self, parentheses=True):
		SmartExpression.__init__(self, parentheses=parentheses)
		return self

	def clear_all_parentheses(self):
		for c in self.children:
			c.clear_all_parentheses()
		self.give_parentheses(False)
		return self

	def auto_parentheses(self):
		pass # Implement in subclasses

	def paren_length(self):
		# Returns the number of glyphs taken up by the expression's potential parentheses.
		# Usually 1 but can be larger for larger parentheses.
		yes_paren = self.copy().give_parentheses(True)
		no_paren = self.copy().give_parentheses(False)
		num_paren_glyphs = len(yes_paren) - len(no_paren)
		assert num_paren_glyphs > 0 and num_paren_glyphs % 2 == 0
		return num_paren_glyphs // 2

	#Man these guys do not work correctly yet
	def nest(self, direction="right"):
		if len(self.children) <= 2:
			return self
		else:
			if direction == "right":
				return type(self)(self.children[0], type(self)(*self.children[1:]))
			elif direction == "left":
				return type(self)(type(self)(*self.children[:-1]), self.children[-1])
			else:
				raise ValueError(f"Invalid direction: {direction}. Must be right or left.")

	def denest(self, denest_all = False, match_type = None):
		if len(self.children) <= 1:
			return self
		if match_type is None:
			match_type = type(self)
		new_children = []
		for child in self.children:
			if type(child) == match_type:
				for grandchild in child.children:
					new_children.append(grandchild.denest(denest_all, match_type))
			elif denest_all:
				new_children.append(child.denest(True, match_type))
			else:
				new_children.append(child)
		return type(self)(*new_children)

	def substitute_at_address(self, subex, address):
		subex = Smarten(subex).copy() #?
		if len(address) == 0:
			return subex
		new_child = self.children[int(address[0])].substitute_at_address(subex, address[1:])
		new_children = self.children[:int(address[0])] + [new_child] + self.children[int(address[0])+1:]
		return type(self)(*new_children)

	def substitute_at_addresses(self, subex, addresses):
		result = self.copy()
		for address in addresses:
			result = result.substitute_at_address(subex, address)
		return result

	def substitute(self, expression_dict):
		result = self.copy()
		for from_subex, to_subex in expression_dict.items():
			result = result.substitute_at_addresses(to_subex, result.get_addresses_of_subex(from_subex))
		return result

	def set_color_by_subex(self, subex_color_dict):
		for subex, color in subex_color_dict.items():
			for ad in self.get_addresses_of_subex(subex):
				self[ad].set_color(color)
				if self.get_subex(ad).parentheses and not subex.parentheses:
					self[ad+"()"].set_color(self.color)
		return self

	def evaluate(self):
		return Smarten(self.compute())

class SmartCombiner(SmartExpression):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		self.symbol = symbol
		self.symbol_glyph_length = symbol_glyph_length
		self.children = list(map(Smarten,children))
		self.left_spacing = ""
		self.right_spacing = ""
		super().__init__(**kwargs)
	
	@tex
	def __str__(self, *args, **kwargs):
		joiner = self.left_spacing + self.symbol + self.right_spacing
		result = joiner.join(["{" + str(child) + "}" for child in self.children])
		return result
	
	def set_spacing(self, left_spacing, right_spacing):
		self.left_spacing = left_spacing
		self.right_spacing = right_spacing

class SmartOperation(SmartCombiner):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		super().__init__(symbol, symbol_glyph_length, *children, **kwargs)

	def compute(self):
		result = self.children[0].compute()
		for child in self.children[1:]:
			result = self.eval_op(result, child.compute())
		return result

class SmartAdd(SmartOperation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda x,y: x+y
		super().__init__("+", 1, *children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative()

class SmartSub(SmartOperation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda x,y: x-y
		super().__init__("-", 1,*children, **kwargs)

	def auto_parentheses(self):
		self.children[0].auto_parentheses()
		for child in self.children[1:]:
			if isinstance(child, (SmartAdd, SmartSub)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative()

class SmartMul(SmartOperation):
	def __init__(self, *children, mode=algebra_config["multiplication_mode"], **kwargs):
		self.eval_op = lambda x,y: x*y
		self.mode = mode
		if mode == "dot":
			super().__init__("\\cdot", 1, *children, **kwargs)
		elif mode == "x":
			super().__init__("\\times", 1, *children, **kwargs)
		elif mode == "juxtapose":
			super().__init__("", 0, *children, **kwargs)
		else:
			raise ValueError("multiplication mode must be dot, x, or juxtapose")

	def auto_parentheses(self): # should be more intelligent based on mode
		for child in self.children:
			if isinstance(child, (SmartAdd, SmartSub)) or child.is_negative():
				child.give_parentheses()
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative()

class SmartDiv(SmartOperation):
	def __init__(self, *children, mode=algebra_config["division_mode"], **kwargs):
		self.eval_op = lambda x,y: x/y
		self.mode = mode
		if mode == "fraction":
			super().__init__("\\over", 1, *children, **kwargs)
		elif mode == "inline":
			super().__init__("\\div", 1, *children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			if (isinstance(child, (SmartAdd, SmartSub, SmartMul, SmartDiv)) or child.is_negative()) and algebra_config["division_mode"] == "inline":
				child.give_parentheses()
			child.auto_parentheses()

	def is_negative(self):
		return self.children[0].is_negative() or self.children[1].is_negative()
	
	def compute(self):
		num = self.children[0].compute()
		den = self.children[1].compute()
		if den == 0:
			raise ZeroDivisionError
		if num % den == 0:
			return int(num / den)
		else:
			return float(num) / float(den)

class SmartPow(SmartOperation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda x,y: x**y
		super().__init__("^", 0, *children, **kwargs)

	def auto_parentheses(self):
		assert len(self.children) == 2 #idc how to auto paren power towers
		if isinstance(self.children[0], SmartOperation) or self.children[0].is_negative():
			self.children[0].give_parentheses()
		for child in self.children:
			child.auto_parentheses()

	def is_negative(self):
		return False

class SmartRelation(SmartCombiner):
	def __init__(self, symbol, symbol_glyph_length, *children, **kwargs):
		super().__init__(symbol, symbol_glyph_length, *children, **kwargs)
	
	def compute(self):
		return all([self.eval_op(self.children[i], self.children[i+1]) for i in range(len(self.children)-1)])

class SmartEquation(SmartRelation):
	def __init__(self, *children, **kwargs):
		self.eval_op = lambda X,Y: X.exactly_equals(Y)
		super().__init__("=", 1, *children, **kwargs)

	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()

class SmartSequence(SmartCombiner):
	def __init__(self, *children, generator=None, **kwargs):
		self.generator = generator
		super().__init__(",", 1, *children, **kwargs)
	
	def auto_parentheses(self):
		for child in self.children:
			child.auto_parentheses()

# Number Classes
class SmartNumber(SmartExpression):
	def __init__(self, **kwargs):
		self.children = []
		super().__init__(**kwargs)

	def compute(self):
		return float(self)

class SmartInteger(SmartNumber):
	def __init__(self, n, **kwargs):
		self.n = n
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return str(self.n)

	def __float__(self):
		return float(self.n)
	
	def compute(self):
		return self.n

	def is_identical_to(self, other):
		return type(self) == type(other) and self.n == other.n

	def is_negative(self):
		return self.n < 0

	@staticmethod
	def GCF(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.n, smartnums))
		return Smarten(int(np.gcd.reduce(nums)))

	@staticmethod
	def LCM(*smartnums):
		smartnums = list(map(Smarten, smartnums))
		nums = list(map(lambda N: N.n, smartnums))
		return Smarten(int(np.lcm.reduce(nums)))

	def prime_factorization(self):
		...

class SmartReal(SmartNumber):
	def __init__(self, x, symbol=None, **kwargs):
		self.x = x
		self.symbol = symbol
		super().__init__(**kwargs)

	@tex
	def __str__(self, decimal_places=4, use_decimal=False):
		if self.symbol and not use_decimal:
			return self.symbol
		rounded = round(self.x, decimal_places)
		if rounded == self.x:
			return str(rounded)
		else:
			return f"{self.x:.{decimal_places}f}" + r"\ldots"

	def __float__(self):
		return float(self.x)

	def is_identical_to(self, other):
		return type(self) == type(other) and self.x == other.x

	def is_negative(self):
		return self.x < 0

class SmartRational(SmartDiv):
	# Better to subclass SmartDiv than SmartNumber because 5/3 is no more a number than 5^3 or 5+3
	# Multiclassing is an option but seems to be more trouble than it's worth
	def __init__(self, a, b, **kwargs):
		if not isinstance(a, (SmartInteger, int)):
			raise TypeError (f"Unsupported numerator type {type(a)}: {a}")
		if not isinstance(b, (SmartInteger, int)):
			raise TypeError (f"Unsupported denominator type {type(b)}: {b}")
		super().__init__(a, b, **kwargs)

	def simplify(self):
		pass #idk will make later

# Odds and Ends
class SmartNegative(SmartExpression):
	def __init__(self, child, **kwargs):
		self.children = [Smarten(child)]
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return "-" + str(self.children[0])

	def auto_parentheses(self):
		if isinstance(self.children[0], (SmartAdd, SmartSub)) or self.children[0].is_negative():
			self.children[0].give_parentheses()
		self.children[0].auto_parentheses()

	def is_negative(self):
		return True

	def compute(self):
		return -self.children[0].compute()

class SmartVariable(SmartExpression):
	def __init__(self, symbol, **kwargs):
		self.symbol = symbol
		self.children = []
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return self.symbol

	def is_identical_to(self, other):
		return type(self) == type(other) and self.symbol == other.symbol

	def compute(self):
		raise ValueError(f"Expression contains a variable {self.symbol}.")

class SmartFunction(SmartExpression):
	def __init__(self, symbol, symbol_glyph_length, rule=None, algebra_rule=None, parentheses_mode="always", **kwargs):
		self.symbol = symbol #string
		self.symbol_glyph_length = symbol_glyph_length #int
		self.rule = rule #callable
		self.children = [] # may be given one child, a sequence which could have multiple children
		self.algebra_rule = algebra_rule #SmE version of rule?
		self.parentheses_mode = parentheses_mode
		self.spacing = ""
		super().__init__(**kwargs)

	@tex
	def __str__(self):
		return self.symbol + self.spacing + (str(self.children[0]) if len(self.children) > 0 else "")

	def __call__(self, *inputs, **kwargs):
		assert len(self.children) == 0, f"Function {self.symbol} cannot be called because it already has children."
		new_func = SmartFunction(self.symbol, self.symbol_glyph_length, self.rule, self.algebra_rule, self.parentheses_mode, **kwargs)
		new_func.children = [SmartSequence(*list(map(Smarten, inputs)), **kwargs)]
		# have to reinitialize SmartExpression and MathTex after setting children for correct indexing and auto_paren.
		super(SmartFunction, new_func).__init__(**kwargs)
		return new_func
	
	def set_spacing(self, spacing):
		self.spacing = spacing
		return self
	
	def auto_parentheses(self):
		if len(self.children) == 0:
			return
		child = self.children[0] #sequence
		if self.parentheses_mode == "always":
			child.give_parentheses(True)
		elif self.parentheses_mode in ["weak", "strong"]:
			if len(child.children) > 1:
				child.give_parentheses(True)
			elif isinstance(child.children[0], (SmartAdd, SmartSub)):
				child.give_parentheses(True)
			else:
				if self.parentheses_mode == "strong":
					if isinstance(child.children[0], SmartOperation):
						child.give_parentheses(True)
		elif self.parentheses_mode == "never":
			child.give_parentheses(False)
		else:
			raise ValueError(f"Unsupported parentheses mode {self.parentheses_mode}.")
		
	def compute(self, *args):
		if len(args) == 0:
			return self.rule(*map(lambda exp: exp.compute(), self.children[0].children))
		else:
			return self.rule(*args)



