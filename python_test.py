from snownlp import SnowNLP
text=r"做工马马虎虎"
s=SnowNLP(text)
print(s.sentiments)