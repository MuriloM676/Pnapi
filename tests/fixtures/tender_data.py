"""
Sample tender data for testing.
"""
sample_tender = {
    "numeroCompra": "123456",
    "processo": "123456/2023",
    "orgaoEntidade": {
        "cnpj": "12345678901234",
        "razaoSocial": "Prefeitura Municipal de São Paulo",
        "ufSigla": "SP"
    },
    "objetoCompra": "Aquisição de equipamentos de informática",
    "modalidadeNome": "Pregão",
    "modalidadeId": 6,
    "valorTotalEstimado": 50000.00,
    "dataAberturaProposta": "20231020",
    "dataEncerramentoProposta": "20231025",
    "numeroControlePNCP": "12345678901234567890"
}

sample_tender_list = {
    "data": [sample_tender],
    "totalRegistros": 1,
    "totalPaginas": 1,
    "numeroPagina": 1
}