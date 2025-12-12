sentence=input("Enter a sentence: ")

character= len(sentence.replace(" "," "))

words=len(sentence.split())

vowels="aeiouAEIOU"
vowel_count=0
for ch in sentence:
    if ch is vowels:
        vowel_count=vowel_count+1

print("number of characters: ",character)
print("number of words: ",words)
print("number od vowels: ",vowel_count)
