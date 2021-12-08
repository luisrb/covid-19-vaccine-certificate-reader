from base45 import b45decode
import zlib
import cbor2
import pprint
from datetime import date


def calculateAge(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


if __name__ == "__main__":
    #The plain text representation of the QR code content
    data = ""

    data = data.replace("HC1:", "")
    z_data = b45decode(data)

    detabytes = bytes(z_data)

    decompress = zlib.decompress(detabytes)
    decoded = cbor2.loads(decompress)
    jsonData = cbor2.loads(decoded.value[2])

    birthDate = jsonData[-260][1]["dob"].split("-")

    data = {
        "name": jsonData[-260][1]["nam"]["gn"],
        "surname": jsonData[-260][1]["nam"]["fn"],
        "Date of birth": jsonData[-260][1]["dob"],
        "Age": calculateAge(date(int(birthDate[0]), int(birthDate[1]), int(birthDate[2]))),
        "State or country": jsonData[-260][1]["v"][0]["co"],
        "Certificate issuer": jsonData[-260][1]["v"][0]["is"],
        "Doses":   str(jsonData[-260][1]["v"][0]["dn"]) + "/" + str(jsonData[-260][1]["v"][0]["sd"]),
    }
    pprint.pprint(data)
