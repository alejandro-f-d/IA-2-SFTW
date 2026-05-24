from typing import Any, Callable, Optional

def resolve(chain: list[Callable], *args, **kwargs) -> Optional[Any]:
    for extractor in chain:
        try:
            value = extractor(*args, **kwargs)
            if value is not None and value != "" and value != []:
                return value
        except Exception:
            continue
    return None

def _paper_title_own(sources: dict, **_) -> Optional[str]:
    return (sources.get("doi_data") or {}).get("titulo")

def _paper_title_wikidata(sources: dict, **_) -> Optional[str]:
    return (sources.get("wikidata") or {}).get("titulo")

def _paper_title_openalex(sources: dict, **_) -> Optional[str]:
    return ((sources.get("openalex") or {}).get("paper") or {}).get("title")


def _paper_doi_own(sources: dict, **_) -> Optional[str]:
    return (sources.get("doi_data") or {}).get("doi")

def _paper_doi_wikidata(sources: dict, **_) -> Optional[str]:
    return (sources.get("wikidata") or {}).get("doi")

def _paper_doi_openalex(sources: dict, **_) -> Optional[str]:
    return ((sources.get("openalex") or {}).get("paper") or {}).get("doi")


def _paper_abstract_own(sources: dict, **_) -> Optional[str]:
    return sources.get("abstract")

def _paper_abstract_openalex(sources: dict, **_) -> Optional[str]:
    return ((sources.get("openalex") or {}).get("paper") or {}).get("abstract")


def _paper_year_wikidata(sources: dict, **_) -> Optional[str]:
    fecha = (sources.get("wikidata") or {}).get("fecha")
    if fecha:
        return fecha[:4]
    return None

def _paper_year_openalex(sources: dict, **_) -> Optional[str]:
    year = ((sources.get("openalex") or {}).get("paper") or {}).get("publication_year")
    return str(year) if year else None


def _paper_citations_wikidata(sources: dict, **_) -> Optional[int]:
    return (sources.get("wikidata") or {}).get("numero_de_citas")

def _paper_citations_openalex(sources: dict, **_) -> Optional[int]:
    return ((sources.get("openalex") or {}).get("paper") or {}).get("citation_count")


def _paper_keywords_openalex(sources: dict, **_) -> Optional[list]:
    kws = ((sources.get("openalex") or {}).get("paper") or {}).get("keywords") or []
    return kws if kws else None

def _paper_keywords_wikidata(sources: dict, **_) -> Optional[list]:
    kws = (sources.get("wikidata") or {}).get("keywords") or []
    clean = [k for k in kws if k and k.strip()]
    return clean if clean else None


def _paper_openalex_id_openalex(sources: dict, **_) -> Optional[str]:
    return ((sources.get("openalex") or {}).get("paper") or {}).get("open_alex_id")

def _person_name_own(sources: dict, person: dict, **_) -> Optional[str]:
    return person.get("nombre_completo")

def _person_name_orcid(sources: dict, person: dict, **_) -> Optional[str]:
    inv = _find_orcid_investigador(sources, person)
    if inv:
        nombre = inv.get("nombre", "")
        apellido = inv.get("apellido", "")
        full = f"{nombre} {apellido}".strip()
        return full if full else None
    return None

def _person_name_openalex(sources: dict, person: dict, **_) -> Optional[str]:
    oa_author = _find_openalex_author(sources, person)
    return (oa_author or {}).get("name")


def _person_orcid_own(sources: dict, person: dict, **_) -> Optional[str]:
    return person.get("orcid")

def _person_orcid_openalex(sources: dict, person: dict, **_) -> Optional[str]:
    oa_author = _find_openalex_author(sources, person)
    return (oa_author or {}).get("orcid")


def _person_email_orcid(sources: dict, person: dict, **_) -> Optional[str]:
    inv = _find_orcid_investigador(sources, person)
    return (inv or {}).get("email")

def _person_wikidata_qid_openalex(sources: dict, person: dict, **_) -> Optional[str]:
    oa_author = _find_openalex_author(sources, person)
    return (oa_author or {}).get("wikidata_qid")

def _org_name_own(sources: dict, org: dict, **_) -> Optional[str]:
    return org.get("institucion")

def _org_name_orcid(sources: dict, org: dict, person: dict, **_) -> Optional[str]:
    emp = _find_orcid_employment(sources, person, org)
    return (emp or {}).get("org_name")

def _org_name_openalex(sources: dict, org: dict, person: dict, **_) -> Optional[str]:
    inst = _find_openalex_institution(sources, person, org)
    return (inst or {}).get("name")

def _org_country_own(sources: dict, org: dict, **_) -> Optional[str]:
    return org.get("pais")

def _org_country_orcid(sources: dict, org: dict, person: dict, **_) -> Optional[str]:
    emp = _find_orcid_employment(sources, person, org)
    return (emp or {}).get("org_country")

def _org_country_openalex(sources: dict, org: dict, person: dict, **_) -> Optional[str]:
    inst = _find_openalex_institution(sources, person, org)
    return (inst or {}).get("country")


def _org_ror_openalex(sources: dict, org: dict, person: dict, **_) -> Optional[str]:
    inst = _find_openalex_institution(sources, person, org)
    return (inst or {}).get("ror_id")

def _org_ror_orcid(sources: dict, org: dict, person: dict, **_) -> Optional[str]:
    emp = _find_orcid_employment(sources, person, org)
    dis_source = (emp or {}).get("org_dis_source", "")
    dis_id = (emp or {}).get("org_dis_id", "")
    if dis_source and "ROR" in dis_source.upper() and dis_id:
        return dis_id
    return None

PAPER_CHAINS = {
    "title":          [_paper_title_own,      _paper_title_wikidata,    _paper_title_openalex],
    "doi":            [_paper_doi_own,        _paper_doi_wikidata,      _paper_doi_openalex],
    "abstract":       [_paper_abstract_own,   _paper_abstract_openalex],
    "year":           [_paper_year_wikidata,  _paper_year_openalex],
    "citation_count": [_paper_citations_wikidata, _paper_citations_openalex],
    "keywords":       [_paper_keywords_wikidata,  _paper_keywords_openalex],
    "open_alex_id":   [_paper_openalex_id_openalex],
}

PERSON_CHAINS = {
    "name":         [_person_name_own,      _person_name_orcid,      _person_name_openalex],
    "orcid":        [_person_orcid_own,     _person_orcid_openalex],
    "email":        [_person_email_orcid],
    "wikidata_qid": [_person_wikidata_qid_openalex],
}

ORG_CHAINS = {
    "name":    [_org_name_own,    _org_name_orcid,    _org_name_openalex],
    "country": [_org_country_own, _org_country_orcid, _org_country_openalex],
    "ror_id":  [_org_ror_orcid,   _org_ror_openalex],
}


def _normalize_name(name: str) -> str:
    replacements = {"á":"a","é":"e","í":"i","ó":"o","ú":"u","ü":"u","ñ":"n"}
    n = name.lower().strip()
    for k, v in replacements.items():
        n = n.replace(k, v)
    return n

def _find_orcid_investigador(sources: dict, person: dict) -> Optional[dict]:
    orcid_own = person.get("orcid")
    nombre_own = _normalize_name(person.get("nombre_completo", ""))

    for orcid_entry in (sources.get("orcid_authors") or []):
        inv = orcid_entry.get("investigador") or {}
        if orcid_own and inv.get("orcid_id") == orcid_own:
            return inv
        inv_full = _normalize_name(f"{inv.get('nombre','')} {inv.get('apellido','')}".strip())
        if inv_full and inv_full == nombre_own:
            return inv
    return None


def _find_orcid_employment(sources: dict, person: dict, org: dict) -> Optional[dict]:
    orcid_own = person.get("orcid")
    org_name_norm = _normalize_name(org.get("institucion", ""))

    for orcid_entry in (sources.get("orcid_authors") or []):
        inv = orcid_entry.get("investigador") or {}
        if orcid_own and inv.get("orcid_id") != orcid_own:
            continue
        for emp in (orcid_entry.get("empleo") or []):
            emp_org_norm = _normalize_name(emp.get("org_name", ""))
            if emp_org_norm and emp_org_norm in org_name_norm or org_name_norm in emp_org_norm:
                return emp
    return None


def _find_openalex_author(sources: dict, person: dict) -> Optional[dict]:
    orcid_own = person.get("orcid")
    nombre_own = _normalize_name(person.get("nombre_completo", ""))

    for author in ((sources.get("openalex") or {}).get("authors") or []):
        if orcid_own and author.get("orcid") == orcid_own:
            return author
        oa_name_norm = _normalize_name(author.get("name", ""))
        if oa_name_norm and oa_name_norm == nombre_own:
            return author
    return None


def _find_openalex_institution(sources: dict, person: dict, org: dict) -> Optional[dict]:
    oa_author = _find_openalex_author(sources, person)
    if not oa_author:
        return None
    org_name_norm = _normalize_name(org.get("institucion", ""))
    for inst in (oa_author.get("institutions") or []):
        inst_norm = _normalize_name(inst.get("name", ""))
        if inst_norm and (inst_norm in org_name_norm or org_name_norm in inst_norm):
            return inst
    return None
