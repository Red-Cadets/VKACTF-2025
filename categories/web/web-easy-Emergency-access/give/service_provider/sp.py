from flask import Flask, request, redirect, render_template_string,render_template, session
import base64, traceback, uuid, zlib, urllib.parse, os, pytz
from dotenv import load_dotenv
from lxml import etree
from signxml import XMLVerifier, InvalidSignature
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template('index.html')

IDP_SSO_URL = os.getenv("IDP_SSO_URL")
SP_ENTITY_ID = os.getenv("SP_ENTITY_ID")
ACS_URL = os.getenv("ACS_URL")

with open("certs/mycert.crt", "r") as f:
    IDP_CERT = f.read()

def generate_saml_request():
    issue_instant = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    request_id = "_" + str(uuid.uuid4())
    nsmap = {
        'samlp': 'urn:oasis:names:tc:SAML:2.0:protocol',
        'saml': 'urn:oasis:names:tc:SAML:2.0:assertion'
    }
    root = etree.Element(
        '{urn:oasis:names:tc:SAML:2.0:protocol}AuthnRequest',
        nsmap=nsmap,
        ID=request_id,
        Version="2.0",
        IssueInstant=issue_instant,
        Destination=IDP_SSO_URL,
        AssertionConsumerServiceURL=ACS_URL
    )
    issuer = etree.SubElement(root, '{urn:oasis:names:tc:SAML:2.0:assertion}Issuer')
    issuer.text = SP_ENTITY_ID
    saml_request = etree.tostring(root, pretty_print=False, xml_declaration=False, encoding="utf-8")
    deflated = zlib.compress(saml_request)[2:-4] 
    return base64.b64encode(deflated).decode()

@app.route("/login")
def login():
    
    saml_request = generate_saml_request()
    saml_request_encoded = urllib.parse.quote_plus(saml_request)
    relay_state = "/collective"

    redirect_url = f"{IDP_SSO_URL}?SAMLRequest={saml_request_encoded}&RelayState={relay_state}"
    return redirect(redirect_url)
    
    
@app.route("/acs", methods=["POST"])
def acs():
    try:
        saml_response_b64 = request.form.get("SAMLResponse", "")
        xml_data = base64.b64decode(saml_response_b64)
        root = etree.fromstring(xml_data)
        
        ns = {
            "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
            "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
            "ds": "http://www.w3.org/2000/09/xmldsig#"
        }

        response_sig = root.find(".//ds:Signature", namespaces=ns)
        
        if response_sig is not None:
            try:
                verified_data_response = XMLVerifier().verify(root, x509_cert=IDP_CERT, id_attribute="ID")
            except InvalidSignature as e:
                return render_template("403.html", error = "Недействительная подпись Response")
        assertions = root.xpath(".//saml:Assertion", namespaces=ns)
        conditions = assertions[-1].find(".//saml:Conditions", namespaces=ns)
        
        if conditions is not None and conditions.attrib.get("NotOnOrAfter"):
            not_on_or_after = conditions.attrib["NotOnOrAfter"]
            expiry_time = datetime.strptime(not_on_or_after, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
            if datetime.utcnow().replace(tzinfo=pytz.UTC) > expiry_time:
                return render_template("403.html", error="SAML истек по времени (NotOnOrAfter)")
        else:
            issue_instant = assertions[-1].attrib.get("IssueInstant")
            if issue_instant:
                issued_time = datetime.strptime(issue_instant, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.UTC)
                if datetime.utcnow().replace(tzinfo=pytz.UTC) - issued_time > timedelta(minutes=5):
                    return render_template("403.html", error="SAML response устарел")        
        
        if not assertions:
            return "Assertion не найдена", 400
        try:
            verified_assertion = XMLVerifier().verify(assertions[-1],x509_cert=IDP_CERT,id_attribute="ID")
        except InvalidSignature as e:
            return render_template("403.html", error = "Недействительная подпись Assertion")
        
        attributes = assertions[0].xpath(".//saml:Attribute", namespaces=ns)
        attribute_map = {}

        for attr in attributes:
            name = attr.attrib.get("Name")
            value_elem = attr.find(".//saml:AttributeValue", namespaces=ns)
            if name and value_elem is not None:
                attribute_map[name] = value_elem.text

        username = attribute_map.get("username", "???")
        role = attribute_map.get("role", "???")
        session["username"] = username
        session["role"] = role
        return redirect("/collective")

    except Exception as e:
        return render_template("500.html", error = "Internal Server Error")

@app.route("/collective")
def collective():
    username = session.get("username")
    role = session.get("role")
    if not username or not role:
        return render_template("403.html")
    FLAG = None
    if role == "Creator":
        with open("flag","r") as f:
            FLAG = f.read()
    return render_template("collective_2.html", username=username, role = role,flag=FLAG)    


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=5000, debug=False)
