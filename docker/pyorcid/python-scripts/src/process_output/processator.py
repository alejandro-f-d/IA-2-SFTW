from dataclasses import dataclass, field
from typing import Optional, Any, Dict
@dataclass
class Researcher:
    orcid_id: str
    orcid_uri: str
    nombre: Optional[str]
    apellido: Optional[str]
    localidad: Optional[str]
    email: Optional[str]
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Researcher":
        orcid_id_info = data.get("orcid-identifier", {})
        orcid_id = orcid_id_info.get("path", "")
        orcid_uri = orcid_id_info.get("uri", "")

        person = data.get("person", {})
        
        name_info = person.get("name", {}) or {}
        given_names = name_info.get("given-names", {}) or {}
        family_name = name_info.get("family-name", {}) or {}
        
        nombre = given_names.get("value")
        apellido = family_name.get("value")

        preferences = data.get("preferences", {})
        localidad = preferences.get("locale")

        emails_info = person.get("emails", {}) or {}
        email_list = emails_info.get("email", []) or []
        email = email_list[0].get("email") if email_list else None # Devolvemos únicamente el primer email.

        return cls(
            orcid_id=orcid_id,
            orcid_uri=orcid_uri,
            nombre=nombre,
            apellido=apellido,
            localidad=localidad,
            email=email
        )

@dataclass
class Employment:
    role_title: Optional[str]
    department: Optional[str]
    org_name: Optional[str]
    org_city: Optional[str]
    org_country: Optional[str]
    org_dis_id: Optional[str]
    org_dis_source: Optional[str]
    start_year: Optional[str]
    end_year: Optional[str]          
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Employment":
        if not data:
            return cls(None, None, None, None, None, None, None, None, None)

        summary = data.get("employment-summary") if "employment-summary" in data else data
        if not isinstance(summary, dict):
            summary = {}

        org           = summary.get("organization") or {}
        address       = org.get("address") or {}
        disambiguated = org.get("disambiguated-organization") or {}
        start_date    = summary.get("start-date") or {}
        end_date      = summary.get("end-date") or {}   

        def get_year(date_dict: dict) -> Optional[str]:
            year_node = date_dict.get("year") or {}
            return year_node.get("value") if isinstance(year_node, dict) else None

        return cls(
            role_title    = summary.get("role-title"),
            department    = summary.get("department-name"),
            org_name      = org.get("name"),
            org_city      = address.get("city"),
            org_country   = address.get("country"),
            org_dis_id    = disambiguated.get("disambiguated-organization-identifier"),
            org_dis_source= disambiguated.get("disambiguation-source"),
            start_year    = get_year(start_date),
            end_year      = get_year(end_date),   
        )

@dataclass
class Publication:
    put_code: Optional[int]
    title: Optional[str]
    pub_type: Optional[str]
    year: Optional[str]
    journal: Optional[str]
    url: Optional[str]
    external_ids: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, ws: Dict[str, Any]) -> "Publication":
        ext_ids = []
        ext_ids_block = ws.get("external-ids", {}) or {}
        ext_id_list = ext_ids_block.get("external-id", []) or []  # era "external-identifier"

        for eid in ext_id_list:
            ext_ids.append({
                "type": eid.get("external-id-type"),
                "value": eid.get("external-id-value"),
            })

        pub_date = ws.get("publication-date", {}) or {}
        year_block = pub_date.get("year", {}) or {}
        year = year_block.get("value")

        return cls(
            put_code=ws.get("put-code"),
            title=((ws.get("title", {}) or {}).get("title", {}) or {}).get("value"),
            pub_type=ws.get("type"),
            year=year,
            journal=(ws.get("journal-title", {}) or {}).get("value"),
            url=(ws.get("url", {}) or {}).get("value"),
            external_ids=ext_ids,
        )


def get_researcher_information(data: dict) -> Researcher:
    return Researcher.from_dict(data)

def get_employment_information(data: dict) -> list[Employment]:
    groups = (
        data.get("activities-summary", {})
            .get("employments", {})
            .get("affiliation-group", []) or []
    )
    result = []
    for group in groups:
        for wrapper in group.get("summaries", []):
            if "employment-summary" in wrapper:
                result.append(Employment.from_dict(wrapper))
    return result

def get_publication_information(data: dict) -> list[Publication]:
    groups = (
        data.get("activities-summary", {})
            .get("works", {})
            .get("group", []) or []
    )
    result = []
    for group in groups:
        for ws in group.get("work-summary", []):
            result.append(Publication.from_dict(ws))
    return result
