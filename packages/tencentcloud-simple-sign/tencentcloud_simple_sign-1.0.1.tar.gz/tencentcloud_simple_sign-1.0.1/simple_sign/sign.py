import datetime
import hashlib
import hmac


def _hmac_sha256(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256)


def _get_signature_key(key, date, service):
    k_date = _hmac_sha256(('TC3' + key).encode('utf-8'), date)
    k_service = _hmac_sha256(k_date.digest(), service)
    k_signing = _hmac_sha256(k_service.digest(), 'tc3_request')
    return k_signing.digest()


def sign(secret_id, secret_key, host, timestamp, expire_timestamp, token=""):
    service = "clbia"
    method = "POST"
    content_type = "application/json"
    canonical_uri = "/"
    canonical_querystring = ""
    canonical_headers = "content-type:%s\nhost:%s\n" % (content_type, host)
    signed_headers = "content-type;host"
    empty_body = b""
    payload_hash = hashlib.sha256(empty_body).hexdigest()
    algorithm = 'TC3-HMAC-SHA256'
    canonical_request = '%s\n%s\n%s\n%s\n%s\n%s' % (method,
                                                    canonical_uri,
                                                    canonical_querystring,
                                                    canonical_headers,
                                                    signed_headers,
                                                    payload_hash)
    digest = hashlib.sha256(canonical_request.encode("utf8")).hexdigest()
    date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
    credential_scope = date + '/' + service + '/tc3_request'
    string2sign = '%s\n%s\n%s\n%s' % (algorithm,
                                      timestamp,
                                      credential_scope,
                                      digest)

    k_date = _hmac_sha256(('TC3' + secret_key).encode('utf-8'), date)
    k_service = _hmac_sha256(k_date.digest(), service)
    k_signing = _hmac_sha256(k_service.digest(), 'tc3_request')

    signing_key = k_signing.digest()
    signature = _hmac_sha256(signing_key, string2sign).hexdigest()
    auth = "TC3-HMAC-SHA256 Credential=%s/%s/%s/tc3_request, SignedHeaders=%s, SignTime=%d, ExpireTime=%d, Signature=%s" % (
        secret_id, date, service, signed_headers, timestamp, expire_timestamp, signature)
    if token:
        auth += ", Token=" + token
    return auth


if __name__ == "__main__":
    expiration = 3600 * 2
    now = 1727685604
    # now = int(time.now())
    secret_id = "test_secret_id"
    secret_key = "test_secret_key"
    token = "test_token"
    service_host = "service-1.test.com"
    sig_expected_token = "TC3-HMAC-SHA256 Credential=test_secret_id/2024-09-30/clbia/tc3_request, SignedHeaders=content-type;host, SignTime=1727685604, ExpireTime=1727692804, Signature=f974c5e4f168d9bd170b6580d573a506ce0acd446e8d71000110269b614e38df, Token=test_token"
    assert sign(secret_id, secret_key, service_host, now, now + expiration, token) == sig_expected_token

    sig_expected = "TC3-HMAC-SHA256 Credential=test_secret_id/2024-09-30/clbia/tc3_request, SignedHeaders=content-type;host, SignTime=1727685604, ExpireTime=1727692804, Signature=f974c5e4f168d9bd170b6580d573a506ce0acd446e8d71000110269b614e38df"
    assert sign(secret_id, secret_key, service_host, now, now + expiration) == sig_expected
