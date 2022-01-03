import requests
import json
import os

ids = []
checked = []

invalid = []
working = []
verified = []
phone = []
billing = []
nitro = []

try: 
    os.mkdir('output') 
except OSError as error: 
    print(error)  

for token in open('tokens.txt', 'r'):
    token = token.strip()
    if len(token) <= 50:
        print('Skipped ' + token)
        continue
    if token in checked:
        continue
    checked.append(token)

    userdata = json.loads(requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': token}).text)
    if 'message' in userdata:
        print(token + ' is invalid. ' + userdata['message'])
        invalid.append(token)
        continue

    if userdata['id'] in ids:
        print('Found user duplicate [' + userdata['id'] + ']')
        continue

    ids.append(userdata['id'])
    working.append(token)

    if userdata['verified']:
        verified.append(token)
    if userdata['phone']:
        phone.append(token)
    if 'premium_type' in userdata:
        if userdata['premium_type'] > 0:
            nitro.append(token)
    
    subscriptions = json.loads(requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers={'authorization': token}).text)
    if str(subscriptions).startswith('[') and len(subscriptions) > 0 and subscriptions[0]['payment_source_id']:
        billing.append(token)
    print(token + ' is Valid.')

print(str(len(working)) + ' Working Tokens')
print(str(len(verified)) + ' Verified Tokens')
print(str(len(phone)) + ' Phone Tokens')
print(str(len(billing)) + ' Billing Tokens')
print(str(len(nitro)) + ' Nitro Tokens')

f = open('output/working.txt', 'w')
f.write('\n'.join([str(e) for e in working]))
f.close()

f = open('output/verified.txt', 'w')
f.write('\n'.join([str(e) for e in verified]))
f.close()

f = open('output/phone.txt', 'w')
f.write('\n'.join([str(e) for e in phone]))
f.close()

f = open('output/billing.txt', 'w')
f.write('\n'.join([str(e) for e in billing]))
f.close()

f = open('output/nitro.txt', 'w')
f.write('\n'.join([str(e) for e in nitro]))
f.close()

f = open('output/invalid.txt', 'w')
f.write('\n'.join([str(e) for e in invalid]))
f.close()