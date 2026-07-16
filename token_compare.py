import tiktoken
from transformers import AutoTokenizer

# this is sample program to compare tokens consumed by various tokenizers.

hindi_list = "है हैँ था थी थे होना हूँ हो हैं मैं हम तुम आप वह यह वे ये क्या क्यों कैसे कब कहाँ कौन किस किसका किसकी किसके "
"और या लेकिन क्योंकि अगर तो फिर भी नहीं हाँ जी अच्छा ठीक बहुत थोड़ा ज्यादा कम सब कोई कुछ हर एक दो तीन चार पाँच "
"घर पानी खाना रोटी दाल चाय दूध फल सब्जी आदमी औरत बच्चा लड़की लड़का दोस्त परिवार माँ पिता भाई बहन बेटा बेटी "
"काम पढ़ाई स्कूल कॉलेज किताब कलम कागज सड़क गाड़ी बस ट्रेन बाजार दुकान पैसा समय दिन रात सुबह शाम आज कल पर अभी "
"चल आ जा बैठ उठ देख सुन बोल लिख पढ़ सोच समझ सीख खेल जीत हार नया पुराना बड़ा छोटा लंबा अच्छा बुरा सही गलत"


eng_list = "is are was was were be am are are i we you you he she it this that they these what why how when where who whom whose "
"and or but because if then again also not yes sir good okay very little more less all someone something every one two three four five "
"house water food bread lentils tea milk fruit vegetable man woman child girl boy friend family mother father brother sister son daughter "
"work study school college book pen paper road vehicle bus train market shop money time day night morning evening today tomorrow on now "
"go come arrive sit stand see hear speak write read think understand learn play win lose new old big small long good bad right wrong"

punj_list ="ਹੈ ਹਨ ਸੀ ਸੀ ਸਨ ਹੋਣਾ ਹਾਂ ਹੋ ਹਨ ਮੈਂ ਅਸੀਂ ਤੂੰ ਤੁਸੀਂ ਉਹ ਇਹ ਉਹ ਇਹ ਕੀ ਕਿਉਂ ਕਿਵੇਂ ਕਦੋਂ ਕਿੱਥੇ ਕੌਣ ਕਿਸ ਕਿਸਦਾ ਕਿਸਦੀ ਕਿਸਦੇ "
"ਅਤੇ ਜਾਂ ਪਰ ਕਿਉਂਕਿ ਜੇ ਤਾਂ ਫਿਰ ਵੀ ਨਹੀਂ ਹਾਂ ਜੀ ਚੰਗਾ ਠੀਕ ਬਹੁਤ ਥੋੜ੍ਹਾ ਜ਼ਿਆਦਾ ਘੱਟ ਸਭ ਕੋਈ ਕੁਝ ਹਰ ਇੱਕ ਦੋ ਤਿੰਨ ਚਾਰ ਪੰਜ "
"ਘਰ ਪਾਣੀ ਖਾਣਾ ਰੋਟੀ ਦਾਲ ਚਾਹ ਦੁੱਧ ਫਲ ਸਬਜ਼ੀ ਆਦਮੀ ਔਰਤ ਬੱਚਾ ਕੁੜੀ ਮੁੰਡਾ ਦੋਸਤ ਪਰਿਵਾਰ ਮਾਂ ਪਿਤਾ ਭਰਾ ਭੈਣ ਪੁੱਤਰ ਧੀ "
"ਕੰਮ ਪੜ੍ਹਾਈ ਸਕੂਲ ਕਾਲਜ ਕਿਤਾਬ ਕਲਮ ਕਾਗਜ਼ ਸੜਕ ਗੱਡੀ ਬੱਸ ਰੇਲ ਬਾਜ਼ਾਰ ਦੁਕਾਨ ਪੈਸਾ ਸਮਾਂ ਦਿਨ ਰਾਤ ਸਵੇਰ ਸ਼ਾਮ ਅੱਜ ਕੱਲ੍ਹ ਉੱਤੇ ਹੁਣ "
"ਚੱਲ ਆ ਜਾ ਬੈਠ ਉੱਠ ਵੇਖ ਸੁਣ ਬੋਲ ਲਿਖ ਪੜ੍ਹ ਸੋਚ ਸਮਝ ਸਿੱਖ ਖੇਡ ਜਿੱਤ ਹਾਰ ਨਵਾਂ ਪੁਰਾਣਾ ਵੱਡਾ ਛੋਟਾ ਲੰਮਾ ਚੰਗਾ ਮਾੜਾ ਸਹੀ ਗਲਤ"


list_of_encodings = tiktoken.list_encoding_names()

# we want to check behavior on each encoding.
ans_list = [];
for encoding in list_of_encodings:
    tokenizer = tiktoken.get_encoding(encoding)
    hindi_tokens = tokenizer.encode(hindi_list)
    eng_token = tokenizer.encode(eng_list)
    punj_token = tokenizer.encode(punj_list)
    ans_list.append((encoding, len(hindi_tokens), len(eng_token), len(punj_token)))   

sarvam_model_name = "sarvamai/sarvam-m"

s_tokenizer = AutoTokenizer.from_pretrained(
                sarvam_model_name,
                trust_remote_code=True,
                fix_mistral_regex=True
                )

s_eng_tokens = s_tokenizer(eng_list, add_special_tokens=False)["input_ids"]
s_hindi_tokens = s_tokenizer(hindi_list, add_special_tokens=False)["input_ids"]
s_punj_tokens = s_tokenizer(punj_list, add_special_tokens=False)["input_ids"]
ans_list.append((sarvam_model_name, len(s_eng_tokens), len(s_hindi_tokens), len(s_punj_tokens)))


print("{:<20} {:<20} {:<20} {:<20}".format('Encoding', 'Eng', 'Hindi', 'Punjabi'))

for encoding, hindi_count, eng_count, punj_count in ans_list:
    print("{:<20} {:<20} {:<20} {:<20}".format(encoding, eng_count, hindi_count, punj_count))
