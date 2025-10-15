"""
Tender model for PNCP API Client.
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OrgaoEntidade:
    """Organization entity model."""
    cnpj: Optional[str] = None
    razaoSocial: Optional[str] = None
    ufSigla: Optional[str] = None


@dataclass
class ItemLicitacao:
    """Item in a tender model."""
    numeroItem: Optional[int] = None
    descricao: Optional[str] = None
    quantidade: Optional[float] = None
    valorUnitario: Optional[float] = None
    valorTotal: Optional[float] = None


@dataclass
class Tender:
    """Tender model."""
    numeroCompra: Optional[str] = None
    processo: Optional[str] = None
    orgaoEntidade: Optional[OrgaoEntidade] = None
    objetoCompra: Optional[str] = None
    modalidadeNome: Optional[str] = None
    modalidadeId: Optional[int] = None
    valorTotalEstimado: Optional[float] = None
    dataAberturaProposta: Optional[str] = None
    dataEncerramentoProposta: Optional[str] = None
    numeroControlePNCP: Optional[str] = None
    itens: List[ItemLicitacao] = field(default_factory=list)
    dataPublicacaoPncp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert tender to dictionary."""
        return {
            "numeroCompra": self.numeroCompra,
            "processo": self.processo,
            "orgaoEntidade": {
                "cnpj": self.orgaoEntidade.cnpj if self.orgaoEntidade else None,
                "razaoSocial": self.orgaoEntidade.razaoSocial if self.orgaoEntidade else None,
                "ufSigla": self.orgaoEntidade.ufSigla if self.orgaoEntidade else None
            } if self.orgaoEntidade else None,
            "objetoCompra": self.objetoCompra,
            "modalidadeNome": self.modalidadeNome,
            "modalidadeId": self.modalidadeId,
            "valorTotalEstimado": self.valorTotalEstimado,
            "dataAberturaProposta": self.dataAberturaProposta,
            "dataEncerramentoProposta": self.dataEncerramentoProposta,
            "numeroControlePNCP": self.numeroControlePNCP,
            "itens": [
                {
                    "numeroItem": item.numeroItem,
                    "descricao": item.descricao,
                    "quantidade": item.quantidade,
                    "valorUnitario": item.valorUnitario,
                    "valorTotal": item.valorTotal
                }
                for item in self.itens
            ] if self.itens else [],
            "dataPublicacaoPncp": self.dataPublicacaoPncp.isoformat() if self.dataPublicacaoPncp else None
        }