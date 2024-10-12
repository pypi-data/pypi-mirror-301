from datetime import date
from decimal import Decimal
from typing import List, Optional, Union
from pydantic import BaseModel, AnyUrl, Field
from .codes import AssessorLevelCode, AssessmentLevelCode, AttestationType, ConformityTopicCode
from .base import Identifier, Measure, BinaryFile, SecureLink, Endorsement, IdentifierScheme, Party, LocationInformation, Address


class Standard(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#standard
    type: str = "Standard"

    id: Optional[AnyUrl]
    name: str
    issuingParty: Identifier
    issueDate: str  #iso8601 datetime string


class Regulation(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#regulation
    type: str = "Regulation"

    id: Optional[AnyUrl]
    name: str
    jurisdictionCountry: str  #countryCode from https://vocabulary.uncefact.org/CountryId
    administeredBy: Identifier
    effectiveDate: str  #iso8601 datetime string


class Metric(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#metric
    type: str = "Metric"

    metricName: str
    metricValue: Measure
    score: Optional[str] = None
    accuracy: Decimal


class Criterion(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#criterion
    type: str = "Criterion"

    id: Optional[AnyUrl]
    name: str
    thresholdValues: List[Metric]


class Facility(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#facility
    type: str = "Facility"

    id: Optional[AnyUrl] # The globally unique ID of the entity as a resolvable URL according to ISO 18975.
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None

    description: Optional[str] = None
    countryOfOpertation:  Optional[str] = None
    processCategory: Optional[str] = None
    operatedByParty: Optional[bool] = None
    otherIdentifier: Optional[str] = None

    #jargon makes it look like a class, schema looks like an attribute. 
    locationInformation: Optional[Union[str, LocationInformation]] = None 
    address: Optional[Address] = None

    IDverifiedByCAB: bool


class Product(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#product
    type: str = "Product"

    id: Optional[AnyUrl]  # The globally unique ID of the entity as a resolvable URL according to ISO 18975.
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None
    serialNumber: Optional[str] = None
    batchNumber: Optional[str] = None
    productImage: Optional[bytes] = None
    description: Optional[str] = None
    productCategory: Optional[str] = None
    furtherInformation: Optional[str] = None
    producedbyParty: Optional[bool] = None
    producedatFacility: Optional[bool] = None
    dimensions: Optional[str] = None
    productionDate: Optional[str] = None
    countryOfProduction: Optional[str] = None
    IDverifiedByCAB: Optional[bool] = None


class ConformityAssessment(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#conformityassessment
    type: str = "ConformityAssessment"

    id: Optional[AnyUrl]
    assessmentDate: date

    referenceStandard: Optional[Standard] = None  #defines the specification
    referenceRegulation: Optional[Regulation] = None  #defines the regulation
    assessmentCriterion: Optional[List[Criterion]] = None  #defines the criteria
    declaredValues: Optional[List[Metric]] = None
    conformance: Optional[bool] = None
    conformityTopic: ConformityTopicCode

    assessedProduct: Optional[List[Product]] = None
    assessedFacility: Optional[List[Facility]] = None
    assessedOrganization: Optional[Party] = None
    auditor: Optional[Party] = None


class ConformityAssessmentScheme(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#conformityassessmentscheme
    type: str = "ConformityAssessmentScheme"

    id: str
    name: str
    issuingParty: Optional[Identifier] = None
    issueDate: Optional[str] = None  #ISO8601 datetime string
    trustmark: Optional[BinaryFile] = None


class ConformityAttestation(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#ConformityAttestation
    type: str = "ConformityAttestation"

    id: str
    name: str
    assessorLevel: Optional[AssessorLevelCode] = None
    assessmentLevel: AssessmentLevelCode
    attestationType: AttestationType
    description: Optional[str] = None  #missing from context file
    issuedToParty: Party
    authorisation: Optional[List[Endorsement]] = None
    conformityCertificate: Optional[SecureLink] = None
    auditableEvidence: Optional[SecureLink] = None
    scope: ConformityAssessmentScheme
    assessment: List[ConformityAssessment]
                                                                      

class CredentialIssuer(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#credentialissuer
    type: str = "CredentialIssuer"

    id: Optional[AnyUrl]
    name: str
    otherIdentifier: Identifier

class DigitalConformityCredential(BaseModel):
    #https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#digitalconformitycredential
    
    context: str = Field(alias="@context")
    id: Optional[AnyUrl]
    issuer: CredentialIssuer
    validFrom: str #DateTime
    validUntil: str #DateTime
    credentialSubject: ConformityAttestation
    credentialSchema: List[dict[str,str]] = {

    }