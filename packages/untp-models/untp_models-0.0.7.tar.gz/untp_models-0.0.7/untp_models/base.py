from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, AnyUrl
from .codes import EncryptionMethod, HashMethod


class IdentifierScheme(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#identifierscheme
    type: str = "IdentifierScheme"

    id: AnyUrl  # from vocabulary.uncefact.org/identifierSchemes
    name: str


class Party(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#Party
    type: str = "Party"

    id: AnyUrl
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None
    # description: str in jargon, but not in context
    registrationCountry: Optional[str] = None
    organizationWebsite: Optional[str] = None
    industryCategory: Optional[str] = None
    otherIdentiifer: Optional[str] = None

class Identifier(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#identifier
    type: str = "Identifier"

    id: AnyUrl
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None


class BinaryFile(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#binaryfile
    type: str = "BinaryFile"

    fileName: str
    fileType: str  # https://mimetype.io/all-types
    file: str  #Base64


class Link(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#link
    type: str = "Link"

    linkURL: AnyUrl
    linkName: str
    linkType: str  # drawn from a controlled vocabulary


class SecureLink(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#securelink
    type: str = "SecureLink"

    linkUrl: AnyUrl
    linkName: str
    linkType: str
    hashDigest: str
    hashMethod: HashMethod
    encryptionMethod: EncryptionMethod


class Measure(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#measure
    type: str = "Measure"

    value: float
    unit: str = Field(
        max_length="3")  # from https://vocabulary.uncefact.org/UnitMeasureCode


class Endorsement(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#endorsement
    type: str = "Endorsement"

    id: AnyUrl
    name: str
    trustmark: Optional[BinaryFile] = None
    issuingAuthority: Identifier
    accreditationCertification: Optional[Link] = None


class Point3D(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#point3d
    type: str = "Point3D"
    data: List[Decimal]

class Point(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#point
    type: str = "Point" 

    coordinates: Point3D


class Point3DWrapper(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#point3dwrapper
    type: str = "Point3DWrapper"

    data: Point3D

class Polygon(BaseModel): 
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#polygon
    type: str = "Polygon" 

    coordinates: Point3DWrapper


class LocationInformation(BaseModel): 
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#location
    type: str = "LocationInformation"

    plusCode: Optional[AnyUrl] = None
    geoLocation: Optional[Point] = None
    geoBoundary: Optional[Polygon] = None

class Address(BaseModel): 
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#address
    type:str = "Address"

    streetAddress: str
    postalCode: str
    addressLocality: str #city/suburb
    addressRegion: str #state/province
    addressCountry: str # ISO-3166 two letter country code. https://vocabulary.uncefact.org/CountryId