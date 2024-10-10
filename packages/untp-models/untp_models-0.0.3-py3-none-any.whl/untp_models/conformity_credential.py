from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, AnyUrl, Field
from .codes import AssessorLevelCode, AssessmentLevelCode, AttestationType, ConformityTopicCode
from .base import Identifier, Measure, BinaryFile, SecureLink, Endorsement, IdentifierScheme, Party, Location, Address


class Standard(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#standard
    type: str = "Standard"

    id: AnyUrl
    name: str
    issuingParty: Identifier
    issueDate: str  #iso8601 datetime string


class Regulation(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#regulation
    type: str = "Regulation"

    id: AnyUrl
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

    id: AnyUrl
    name: str
    thresholdValues: Metric


class Facility(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#facility
    type: str = "Facility"

    # this looks wrongs
    id: AnyUrl  # The globally unique ID of the entity as a resolvable URL according to ISO 18975.
    name: str
    registeredId: Optional[str] = None
    idScheme: Optional[IdentifierScheme] = None

    description: Optional[str] = None
    countryOfOpertation:  Optional[str] = None
    processCategory: Optional[str] = None
    operatedByParty: Optional[bool] = None
    otherIdentifier: Optional[str] = None

    locationInformation: Optional[Location]
    address: Optional[Address]

    IDverifiedByCAB: bool


class Product(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#product
    type: str = "Product"

    id: AnyUrl  # The globally unique ID of the entity as a resolvable URL according to ISO 18975.
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

    id: AnyUrl
    assessmentDate: date

    referenceStandard: Optional[Standard] = None  #defines the specification
    referenceRegulation: Optional[Regulation] = None  #defines the regulation
    assessmentCriterion: Optional[Criterion] = None  #defines the criteria
    declaredValues: Optional[List[Metric]] = None
    conformance: Optional[bool] = None
    conformityTopic: ConformityTopicCode

    assessedProducts: Optional[Product] = None
    assessedFacilities: Optional[Facility] = None
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
    authorisation: Optional[Endorsement] = None
    conformityCertificate: Optional[SecureLink] = None
    auditableEvidence: Optional[SecureLink] = None
    scope: ConformityAssessmentScheme
    assessment: ConformityAssessment


class CredentialIssuer(BaseModel):
    # https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#credentialissuer
    type: str = "CredentialIssuer"

    id: AnyUrl
    name: str
    otherIdentifier: Identifier

class DigitalConformityCredential(BaseModel):
    #https://jargon.sh/user/unece/ConformityCredential/v/0.5.0/artefacts/readme/render#digitalconformitycredential
    context: str = Field(alias="@context")
    id: AnyUrl
    issuer: CredentialIssuer
    validFrom: str #DateTime
    validUntil: str #DateTime
    credentialSubject: ConformityAttestation