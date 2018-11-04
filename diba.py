#!/usr/bin/env python3
import requests
import hashlib
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 
import uuid
import arrow
from ipdb import set_trace

cert_pub = "certs/server_public2.crt"
cert_priv = "certs/server2.key"
sign_key = "certs/server.key"

client_id = "fdcb31b7-e33b-42b2-b4a6-4e7f14d1a3cc"
api_base = "https://api.ing.com%s" # %s !

def gen_request_date():
    now = arrow.utcnow().format("ddd, DD MMM YYYY HH:mm:ss")
    now = "{} GMT".format(now)
    #print(now)
    return now


def calc_digest(message):
    m = hashlib.sha256()
    m.update(message.encode())
    digest = b64encode(m.digest()).decode()
    #print(digest)
    return digest


def calc_signature(method, endpoint, date, digest, req_id):
    signing_string = """(request-target): {} {}\ndate: {}\ndigest: SHA-256={}\nx-ing-reqid: {}""".format(method, endpoint, date, digest, req_id)
    #print("signing_string: \n{}".format(signing_string))
    signing_string_signed = sign(signing_string)
    #print(signing_string_signed)
    return signing_string_signed


def sign(signing_string):
    key = open(sign_key, "r").read() 
    rsakey = RSA.importKey(key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    digest.update(signing_string.encode())
    sign = signer.sign(digest) 
    sign = b64encode(sign).decode()
    #print(b64encode(sign))
    return sign


def get_access_token():
    endpoint = "/oauth2/token"
    method = "POST"
    #body = "grant_type=client_credentials&scope=granting+greetings%3Aview"
    body = "grant_type=client_credentials"
    json = build_request(method, endpoint, body)
    access_token = json['access_token']
    return access_token


def showcase():
    access_token = get_access_token()
    print("got the access_token", access_token)
    endpoint = "/greetings/single"
    method = "GET"
    json = build_request(method, endpoint, access_token=access_token)


def build_request(method, endpoint, data="", access_token=None):
    req_id = str(uuid.uuid4())
    date = gen_request_date()
    digest = calc_digest(data)
    cert=(cert_pub, cert_priv)
    headers = {
            "Date": date,
            "Digest": "SHA-256={}".format(digest), 
            "X-ING-ReqID": req_id,
            "Authorization": 'Signature keyId="{}",algorithm="rsa-sha256",headers="(request-target) date digest x-ing-reqid",signature="{}"'.format(client_id, calc_signature(method.lower(), endpoint, date, digest, req_id)),
              }
    if access_token:
        headers.update({
                "Authorization": "Bearer {}".format(access_token),
                "Content-Type": "application/json"})
    else:
        headers.update({
                "Content-Type": "application/x-www-form-urlencoded"})
    resp = requests.request(method.upper(), api_base % endpoint, headers=headers, data=data, cert=cert)
    print(resp.text)
    json = resp.json()
    return resp.json()


#assert calc_digest(""), "47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

#get_access_token()
showcase()
