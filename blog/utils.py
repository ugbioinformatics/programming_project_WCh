from typing import Optional, List
import json
import requests

UNIPROT_URL = "https://www.uniprot.org/uniprot/{}.fasta"


def get_uniprot_file(uniprot_id: str, header=False) -> Optional[str]:
    """Returns a fasta file from uniprot.org for the given uniprot_id."""
    url = UNIPROT_URL.format(uniprot_id)
    response = requests.get(url)
    if response.ok:
        if header:
            _header = response.text.split("\n")[0]
            return _header
        return response.text

    return None


def search_uniprot(query: str, format: str, fields: Optional[List[str]]=[], reviewed: bool = True, limit: int = 10) -> \
        Optional[List[str]]:
    """Returns a fasta file from uniprot.org for the given query."""
    url = "https://rest.uniprot.org/uniprotkb/search"
    query += " AND (reviewed:true)" if reviewed else ""
    if format not in ['tsv', 'xslx', 'json']:
        fields = []

    params = {
        "query": query,
        "format": format,
        "fields": ",".join(fields),
        "size": limit,
    }
    
#    import logging
#    logging.basicConfig()
#    logger = logging.getLogger(__name__)
    
    response = requests.get(url, params=params)
    if response.ok:
        data = response.text
#        logger.warning("test logowanie")
#        logger.warning(data=="")
        if data.startswith("<!doctype html>"):
            return None
        if format == 'list' and data !="":
            results = data.split("\n")
        elif format == 'json':
            results = json.loads(data)
        else:
            results = data
        return results

    return None
