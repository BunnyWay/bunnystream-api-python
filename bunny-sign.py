from urllib.parse import urlparse, parse_qs
import hashlib, time, base64

def sign_bcdn_url(url, security_key, path_allowed=None, is_directory_token=False, expiration_time=3600, user_ip=None, countries_allowed=None, countries_blocked=None, referers_allowed=None):
    if countries_allowed is not None:
        url += '?' if urlparse(url).query == "" else '&'
        url += f'token_countries={countries_allowed}'
    
    if countries_blocked is not None:
        url += '?' if urlparse(url).query == "" else '&'
        url += f'token_countries_blocked={countries_blocked}'
    
    if referers_allowed is not None:
        url += '?' if urlparse(url).query == "" else '&'
        url += f'token_referer={referers_allowed}'
    
    url_scheme = urlparse(url).scheme
    url_host = urlparse(url).hostname
    url_path = urlparse(url).path
    url_query = urlparse(url).query

    parameters = parse_qs(url_query)
    
    signature_path = url_path
    if path_allowed is not None:
        signature_path = path_allowed
        parameters["token_path"] = signature_path
    
    expires = int(time.time()) + expiration_time

    parameters = dict(sorted(parameters.items()))

    parameter_data = ''
    parameter_data_url = ''
    
    for key, value in parameters.items():
        parameter_data += f'{key}={value}'
        urlvalue = value.replace('/', '%2F')
        parameter_data_url += f'&{key}={urlvalue}'

    hashable_base = security_key + signature_path + str(expires)
    
    if user_ip is not None:
        hashable_base += user_ip
    
    hashable_base += parameter_data
    token = hashlib.sha256(hashable_base.encode()).digest()
    token = base64.b64encode(token).decode()
    token = token.replace('+', '-').replace('/', '_').rstrip('=')
    
    if is_directory_token:
        return f'{url_scheme}://{url_host}/bcdn_token={token}&expires={expires}{parameter_data_url}{url_path}'
    else:
        return f'{url_scheme}://{url_host}{url_path}?token={token}{parameter_data_url}&expires={expires}'

