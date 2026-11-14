from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class PersonalInfoModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    phone: str | None = None
    address: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None


class ExperienceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str = Field(min_length=1)
    position: str = Field(min_length=1)
    start_date: date
    end_date: date | None = None
    description: str


class EducationModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    institution: str = Field(min_length=1)
    degree: str = Field(min_length=1)
    field_of_study: str | None = None
    start_date: date
    end_date: date | None = None


class CertificationModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    issuer: str = Field(min_length=1)
    issue_date: date
    expiry_date: date | None = None


class ParsedResumePayloadModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    personal_info: PersonalInfoModel
    summary: str | None = None
    experience: list[ExperienceModel]
    education: list[EducationModel] = Field(default_factory=list)
    skills: list[str]
    certifications: list[CertificationModel] = Field(default_factory=list)
