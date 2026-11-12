import json
import re
from typing import Any

from llm.llm_service import ChatMessage, LLMService, StructuredGenerationRequest

from core.errors import LlmProcessingError
from core.validation.schema_validation import load_resume_schema

_EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_PATTERN = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")
_URL_PATTERN = re.compile(r"https?://[^\s)>,]+")
_SKILL_SEPARATOR = re.compile(r"[,;|•·\n]+")
_PERSONAL_FIELDS = (
    "name",
    "email",
    "phone",
    "address",
    "linkedin_url",
    "github_url",
)
_SECTION_ALIASES = {
    "summary": "summary",
    "professional summary": "summary",
    "profile": "summary",
    "objective": "summary",
    "experience": "experience",
    "work experience": "experience",
    "professional experience": "experience",
    "employment history": "experience",
    "education": "education",
    "skills": "skills",
    "technical skills": "skills",
    "core skills": "skills",
    "certifications": "certifications",
    "licenses": "certifications",
    "certifications and licenses": "certifications",
}


def _empty_payload() -> dict[str, Any]:
    return {
        "personal_info": {
            field: "" if field in {"name", "email"} else None
            for field in _PERSONAL_FIELDS
        },
        "summary": None,
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
    }


def _normalize_heading(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.strip().lower()).strip()


def _split_inline_heading(line: str) -> tuple[str | None, str | None]:
    if ":" not in line:
        return None, None
    heading, content = line.split(":", 1)
    canonical = _SECTION_ALIASES.get(_normalize_heading(heading))
    return canonical, content.strip() or None


def _extract_sections(lines: list[str]) -> dict[str, list[str]]:
    sections = {name: [] for name in set(_SECTION_ALIASES.values())}
    current_section: str | None = None

    for line in lines:
        inline_heading, inline_content = _split_inline_heading(line)
        heading = inline_heading or _SECTION_ALIASES.get(_normalize_heading(line))

        if heading is not None:
            current_section = heading
            if inline_content:
                sections[current_section].append(inline_content)
            continue

        if current_section is not None:
            sections[current_section].append(line)

    return sections


def _find_name(lines: list[str]) -> str:
    for line in lines:
        if _SECTION_ALIASES.get(_normalize_heading(line)) is not None:
            continue
        if _split_inline_heading(line)[0] is not None:
            continue
        if line.startswith(("-", "*", "•")):
            continue
        if any(pattern.search(line) for pattern in (_EMAIL_PATTERN, _URL_PATTERN)):
            continue

        candidate = line.split("|", 1)[0].strip()
        if (
            candidate
            and len(candidate) <= 80
            and candidate.count(" ") <= 6
            and not candidate.endswith(".")
        ):
            return candidate

    return ""


def _find_phone(text: str) -> str | None:
    for match in _PHONE_PATTERN.finditer(text):
        candidate = match.group(0).strip()
        digit_count = len(re.sub(r"\D", "", candidate))
        if 10 <= digit_count <= 15:
            return candidate
    return None


def _find_url(text: str, host: str) -> str | None:
    for url in _URL_PATTERN.findall(text):
        if host in url.lower():
            return url.rstrip(".,;")
    return None


def _join_section(lines: list[str]) -> str | None:
    text = " ".join(line.strip() for line in lines).strip()
    return text or None


def _extract_skills(lines: list[str]) -> list[str]:
    skills: list[str] = []
    for item in _SKILL_SEPARATOR.split("\n".join(lines)):
        skill = item.strip(" -*•\t")
        if skill and skill not in skills:
            skills.append(skill)
    return skills


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _merge_personal_info(
    deterministic: dict[str, Any],
    llm_payload: dict[str, Any],
) -> dict[str, Any]:
    deterministic_info = deterministic.get("personal_info", {})
    llm_info = llm_payload.get("personal_info", {})

    return {
        field: (
            deterministic_info.get(field)
            if _has_value(deterministic_info.get(field))
            else llm_info.get(field)
        )
        for field in _PERSONAL_FIELDS
    }


def _merge_list(deterministic: list[Any], llm_value: list[Any]) -> list[Any]:
    if _has_value(deterministic):
        return list(deterministic)
    return list(llm_value or [])


def _merge_skills(deterministic: list[Any], llm_value: list[Any]) -> list[str]:
    merged: list[str] = []
    for item in [*(deterministic or []), *(llm_value or [])]:
        if isinstance(item, str) and item.strip() and item not in merged:
            merged.append(item)
    return merged


def resolve_parsing_model(llm_service: LLMService) -> str:
    try:
        if not llm_service.check_availability():
            raise LlmProcessingError("LLM service is unavailable.")
        models = llm_service.list_models()
    except LlmProcessingError:
        raise
    except Exception as exc:
        raise LlmProcessingError("LLM models could not be listed.") from exc

    if not models:
        raise LlmProcessingError("No LLM models are available.")

    return models[0].name


def extract_deterministic_data(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    sections = _extract_sections(lines)
    payload = _empty_payload()
    personal_info = payload["personal_info"]

    personal_info["name"] = _find_name(lines)

    email_match = _EMAIL_PATTERN.search(text)
    if email_match:
        personal_info["email"] = email_match.group(0)

    personal_info["phone"] = _find_phone(text)

    personal_info["linkedin_url"] = _find_url(text, "linkedin.com")
    personal_info["github_url"] = _find_url(text, "github.com")

    payload["summary"] = _join_section(sections["summary"])
    payload["skills"] = _extract_skills(sections["skills"])

    return payload


def merge_resume_payloads(
    deterministic: dict[str, Any],
    llm_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "personal_info": _merge_personal_info(deterministic, llm_payload),
        "summary": (
            deterministic.get("summary")
            if _has_value(deterministic.get("summary"))
            else llm_payload.get("summary")
        ),
        "experience": _merge_list(
            deterministic.get("experience", []),
            llm_payload.get("experience", []),
        ),
        "education": _merge_list(
            deterministic.get("education", []),
            llm_payload.get("education", []),
        ),
        "skills": _merge_skills(
            deterministic.get("skills", []),
            llm_payload.get("skills", []),
        ),
        "certifications": _merge_list(
            deterministic.get("certifications", []),
            llm_payload.get("certifications", []),
        ),
    }


def enhance_with_llm(
    text: str,
    deterministic_payload: dict[str, Any],
    llm_service: LLMService,
    model: str,
) -> dict[str, Any]:
    request = StructuredGenerationRequest(
        model=model,
        messages=[
            ChatMessage(
                role="system",
                content=(
                    "You extract structured resume data. Return only JSON that "
                    "matches the provided schema. Do not invent facts. Use null "
                    "for unknown optional values and dates in YYYY-MM-DD format."
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    "Extracted resume text:\n\n"
                    f"{text}\n\n"
                    "Deterministic draft:\n"
                    f"{json.dumps(deterministic_payload, indent=2)}\n\n"
                    "Return the complete structured resume payload."
                ),
            ),
        ],
        json_schema=load_resume_schema(),
    )

    try:
        response = llm_service.generate_structured(request)
    except Exception as exc:
        raise LlmProcessingError("LLM resume enhancement failed.") from exc

    if not isinstance(response, dict):
        raise LlmProcessingError("LLM response was not a structured resume payload.")

    return response


def parse_resume_text(
    text: str,
    llm_service: LLMService,
    model: str,
) -> dict[str, Any]:
    try:
        deterministic = extract_deterministic_data(text)
    except Exception:
        deterministic = _empty_payload()

    llm_payload = enhance_with_llm(text, deterministic, llm_service, model)
    return merge_resume_payloads(deterministic, llm_payload)
