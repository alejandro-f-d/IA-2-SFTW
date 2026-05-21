from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
@dataclass
class Paper:
    open_alex_id: Optional[str]       
    title: Optional[str]              
    doi: Optional[str]                
    publication_year: Optional[int]   
    citation_count: Optional[int]     
    abstract: Optional[str]          
    keywords: List[str] = field(default_factory=list)  

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Paper":
        abstract = _reconstruct_abstract(data.get("abstract_inverted_index"))
        keywords = []
        for kw in data.get("keywords", []) or []:
            if isinstance(kw, dict):
                val = kw.get("keyword") or kw.get("display_name")
            else:
                val = str(kw)
            if val:
                keywords.append(val)
        return cls(
            open_alex_id=data.get("id"),
            title=data.get("title"),
            doi=data.get("doi"),
            publication_year=data.get("publication_year"),
            citation_count=data.get("cited_by_count"),
            abstract=abstract,
            keywords=keywords,
        )
@dataclass
class Author:
    open_alex_author_id: Optional[str]
    name: Optional[str]              
    orcid: Optional[str]             
    wikidata_qid: Optional[str]      
    institutions: List[Dict] = field(default_factory=list)  
    @classmethod
    def from_authorship(cls, authorship: Dict[str, Any]) -> "Author":
        author_obj = authorship.get("author") or {}
        orcid_raw = author_obj.get("orcid")  
        orcid = _clean_orcid(orcid_raw)
        wikidata_qid = None
        for alt_id in (author_obj.get("ids") or {}):
            pass  
        institutions = []
        for inst in (authorship.get("institutions") or []):
            institutions.append({
                "open_alex_inst_id": inst.get("id"),
                "name": inst.get("display_name"),
                "ror_id": inst.get("ror"),       
                "country": inst.get("country_code"),  
            })
        return cls(
            open_alex_author_id=author_obj.get("id"),
            name=author_obj.get("display_name"),
            orcid=orcid,
            wikidata_qid=wikidata_qid,
            institutions=institutions,
        )
@dataclass
class Concept:
    open_alex_concept_id: Optional[str]   
    display_name: Optional[str]           
    score: Optional[float]                
    level: Optional[int]                  
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Concept":
        return cls(
            open_alex_concept_id=data.get("id"),
            display_name=data.get("display_name"),
            score=data.get("score"),
            level=data.get("level"),
        )
def get_paper_information(data: Dict[str, Any]) -> Paper:
    return Paper.from_dict(data)
def get_authors_information(data: Dict[str, Any]) -> List[Author]:
    authorships = data.get("authorships") or []
    return [Author.from_authorship(a) for a in authorships]
def get_concepts_information(data: Dict[str, Any]) -> List[Concept]:
    concepts = []
    for c in (data.get("concepts") or []):
        concepts.append(Concept.from_dict(c))
    existing_ids = {c.open_alex_concept_id for c in concepts}
    for t in (data.get("topics") or []):
        t_id = t.get("id")
        if t_id not in existing_ids:
            concepts.append(Concept(
                open_alex_concept_id=t_id,
                display_name=t.get("display_name"),
                score=t.get("score"),
                level=t.get("subfield", {}).get("id") if isinstance(t.get("subfield"), dict) else None,
            ))
    return concepts
def get_citations_information(data: Dict[str, Any]) -> List[str]:
    return list(data.get("referenced_works") or [])
def _reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
    if not inverted_index:
        return None
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(word for _, word in word_positions)

def _clean_orcid(orcid_url: Optional[str]) -> Optional[str]:
    if not orcid_url:
        return None
    return orcid_url.replace("https://orcid.org/", "").strip()
