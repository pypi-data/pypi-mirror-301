# ამ ფუნქციის საშუალებით შესაძლებელია სამაგისტრო საფეხურის საგრანტო/ნორმირებული ქულის გამოთვლა გამოცდაზე მიღებული ქულების შეყვანით.
class NormalPoint():
	def __init__(self, math, log, read, write):
		self.norm_math = math/19
		self.norm_log = log/17
		self.norm_read = read/21
		self.norm_write = write/18

	def abs_norm_point(self):
		absolute = (self.norm_math + self.norm_log + self.norm_read + self.norm_write) * 40698000
		return (f"Your normal point is: {absolute}.")

# მაგალითად
student1 = NormalPoint(13, 7.8, 19.8, 14)
print(student1.abs_norm_point())
#მიღებულ შედეგს სტუდენტი შეადარებს შესაბამისი მიმართულების საგრანტო კონკურსის მინიმალურ ქულას და გაიგებს, მოხვდა თუ არა ის სიაში.



