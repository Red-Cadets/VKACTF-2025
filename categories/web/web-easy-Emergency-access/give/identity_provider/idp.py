from flask import Flask, request, render_template, session
from datetime import datetime, timedelta
from urllib.parse import unquote
import base64, os, uuid, zlib, json
import lxml.etree as ET
from dotenv import load_dotenv
from lxml import etree
from signxml import XMLSigner, XMLVerifier, SignatureConstructionMethod, methods
from xml.dom import minidom
from pathlib import Path

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

def decode_saml_request(encoded_request):
    decoded = base64.b64decode(unquote(encoded_request))
    try:
        inflated = zlib.decompress(decoded, -15)
    except zlib.error:
        inflated = decoded
    return etree.fromstring(inflated)

def sign_xml(xml_string: str, key_path: str, cert_path: str) -> str:
    private_key = Path(key_path).read_text()
    certificate = Path(cert_path).read_text()

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.fromstring(xml_string.encode("utf-8"), parser)

    if not root.tag.endswith("Response"):
        raise ValueError("Ожидался корневой элемент <Response>")

    signer = XMLSigner(
        method=SignatureConstructionMethod.enveloped,
        c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"
    )

    ns = {"saml": "urn:oasis:names:tc:SAML:2.0:assertion"}
    assertion = root.find(".//saml:Assertion", namespaces=ns)
    if assertion is None:
        raise ValueError("Assertion не найдена")

    signed_assertion = signer.sign(assertion, key=private_key, cert=certificate)

    parent = assertion.getparent()
    parent.replace(assertion, signed_assertion)

    signed_response = signer.sign(root, key=private_key, cert=certificate)

    issuer = signed_response.find("{*}Issuer")
    status = signed_response.find("{*}Status")
    signature = signed_response.find("{http://www.w3.org/2000/09/xmldsig#}Signature")

    if signature is not None:
        signed_response.remove(signature)
        if issuer is not None:
            signed_response.insert(signed_response.index(issuer) + 1, signature)
        else:
            signed_response.insert(0, signature)

    return etree.tostring(signed_response, pretty_print=False, encoding="unicode")

def generate_saml_response(username, password, in_response_to, acs_url, sp_issuer,role):
    now = datetime.utcnow()
    issue_instant = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    not_before = (now - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    not_on_or_after = (now + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    session_expiry = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    response_id = "_" + str(uuid.uuid4())
    assertion_id = "_" + str(uuid.uuid4())
    session_index = "_" + str(uuid.uuid4())

    destination = acs_url
    issuer = sp_issuer
    name_id = str(uuid.uuid4())

    NSMAP = {
        'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol',
        'saml': 'urn:oasis:names:tc:SAML:2.0:assertion',
        'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }

    ET.register_namespace('samlp', NSMAP['samlp'])
    ET.register_namespace('saml', NSMAP['saml'])
    ET.register_namespace('ds', NSMAP['ds'])

    response = ET.Element('{%s}Response' % NSMAP['samlp'], {
        'ID': response_id,
        'Version': '2.0',
        'IssueInstant': issue_instant,
        'Destination': destination,
        'InResponseTo': in_response_to,
    })

    issuer_el = ET.SubElement(response, '{%s}Issuer' % NSMAP['saml'])
    issuer_el.text = issuer

    status = ET.SubElement(response, '{%s}Status' % NSMAP['samlp'])
    status_code = ET.SubElement(status, '{%s}StatusCode' % NSMAP['samlp'], {
        'Value': 'urn:oasis:names:tc:SAML:2.0:status:Success'
    })

    assertion = ET.SubElement(response, '{%s}Assertion' % NSMAP['saml'], {
        'ID': assertion_id,
        'IssueInstant': issue_instant,
        'Version': '2.0'
    })

    issuer_in_assertion = ET.SubElement(assertion, '{%s}Issuer' % NSMAP['saml'])
    issuer_in_assertion.text = issuer

    subject = ET.SubElement(assertion, '{%s}Subject' % NSMAP['saml'])
    name_id_el = ET.SubElement(subject, '{%s}NameID' % NSMAP['saml'])
    name_id_el.text = name_id

    subject_conf = ET.SubElement(subject, '{%s}SubjectConfirmation' % NSMAP['saml'], {
        'Method': 'urn:oasis:names:tc:SAML:2.0:cm:bearer'
    })
    subject_conf_data = ET.SubElement(subject_conf, '{%s}SubjectConfirmationData' % NSMAP['saml'], {
    'InResponseTo': in_response_to,
    'NotOnOrAfter': not_on_or_after,
    'Recipient': destination
    })

    conditions = ET.SubElement(assertion, '{%s}Conditions' % NSMAP['saml'], {
        'NotBefore': not_before,
        'NotOnOrAfter': not_on_or_after
    })

    audience_restriction = ET.SubElement(conditions, '{%s}AudienceRestriction' % NSMAP['saml'])
    audience = ET.SubElement(audience_restriction, '{%s}Audience' % NSMAP['saml'])
    audience.text = destination

    authn_statement = ET.SubElement(assertion, '{%s}AuthnStatement' % NSMAP['saml'], {
        'AuthnInstant': issue_instant,
        'SessionIndex': session_index,
        'SessionNotOnOrAfter': session_expiry
    })

    authn_context = ET.SubElement(authn_statement, '{%s}AuthnContext' % NSMAP['saml'])
    class_ref = ET.SubElement(authn_context, '{%s}AuthnContextClassRef' % NSMAP['saml'])
    class_ref.text = "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport"
    audience.text = sp_issuer
    attribute_statement = ET.SubElement(assertion, '{%s}AttributeStatement' % NSMAP['saml'])

    for attr_name, attr_value in {
        "role": role,
        "username": username,
        "password": password,
    }.items():
        attr_el = ET.SubElement(attribute_statement, '{%s}Attribute' % NSMAP['saml'], {
            'Name': attr_name
        })
        attr_value_el = ET.SubElement(attr_el, '{%s}AttributeValue' % NSMAP['saml'])
        attr_value_el.text = attr_value

    xml_str = ET.tostring(response, encoding="utf-8", method="xml")
    signed_xml = sign_xml(xml_str.decode("utf-8"), 'certs/mykey.pem', 'certs/mycert.crt')   

    sign_b64 = base64.b64encode(signed_xml.encode("utf-8"))  
    return signed_xml

@app.route("/sso")
def idp_login():
    saml_request = request.args.get("SAMLRequest")
    relay_state = request.args.get("RelayState")

    if not saml_request:
        return render_template("400.html", error="Missing SAMLRequest")

    try:
        saml_xml = decode_saml_request(saml_request)
        request_id = saml_xml.get("ID")
        acs_url = saml_xml.get("AssertionConsumerServiceURL")
        issuer_el = saml_xml.find(".//{urn:oasis:names:tc:SAML:2.0:assertion}Issuer")
        issuer = issuer_el.text if issuer_el is not None else "Unknown"
    except Exception as e:
        return render_template("400.html",error = "Invalid SAMLRequest")
    session["acs_url"] = acs_url
    session["request_id"] = request_id
    session["relay_state"] = relay_state
    session["sp_issuer"] = issuer
    return render_template("loginpass.html")

@app.route("/sso/login", methods=["POST"])
def sso_login_post():
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    if len(username) < 3:
        return render_template("loginpass.html", error="Имя пользователя слишком короткое (минимум 3 символа).")

    if len(password) < 8:
        return render_template("loginpass.html", error="Пароль слишком короткий (минимум 8 символов).")


    with open("users.json", encoding="utf-8") as f:
        users_db = json.load(f)
    
    user = users_db.get(username)

    if not user or user["password"] != password:
        return render_template("loginpass.html", error="Неверный логин или пароль")

    acs_url = session.get("acs_url")
    request_id = session.get("request_id")
    relay_state = session.get("relay_state")
    sp_issuer = session.get("sp_issuer")
    if not acs_url or not request_id:
        return render_template("400.html", error = "Сессия истекла или нарушена")
    saml_response = generate_saml_response(
        username = username, 
        password = password, 
        in_response_to = request_id, 
        acs_url = acs_url, 
        sp_issuer = sp_issuer,
        role = user["role"])
    
    saml_b64 = base64.b64encode(saml_response.encode('utf-8')).decode('utf-8')
    session.pop("acs_url", None)
    session.pop("request_id", None)
    session.pop("relay_state", None)
    session.pop("sp_issuer", None)
    return render_template("redirect.html", acs_url=acs_url, saml_b64=saml_b64, relay_state=relay_state)



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001, debug=False)
