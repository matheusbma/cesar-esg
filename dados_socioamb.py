import pandas as pd

df = pd.DataFrame(
    {
        "Indicador": [
            "Consumo mensal de Energia Elétrica",
            "Proporção de Energia elétrica consumida do Mercado Livre",
            "Proporção de Energia elétrica consumida do Mercado Cativo",
            "Peso total de resíduos sólidos produzidos",
            "Gravimetrida dos resíduos sólidos (Orgânicos e rejeitos)",
            "Gravimetrida dos resíduos sólidos (Papel/Papelão)",
            "Gravimetrida dos resíduos sólidos (Plástico)",
            "Gravimetrida dos resíduos sólidos (Metais)",
            "Gravimetrida dos resíduos sólidos (Eletrônicos)",
            "Gravimetrida dos resíduos sólidos (Pilhas e baterias)",
            "Proporção de Resíduos destinados ao aterro",
            "Proporção de resíduos destindos à reciclagem",
            "Consumo Mensal de Água",
            "Proporção da água tratada que é consumida",
            "Consumo mensal de combustível",
            "Qualidade do ar no ambiente de trabalho",
            "Resíduos Eletrônicos",
            "Pilhas",
        ],

        "Unidade": [
            "115 KW",
            "46,7%",
            "53,3%",
            "3.950Kg",
            "1.263 kg",
            "1.841kg",
            "257kg",
            "72 kg",
            "505kg",
            "12kg",
            "32%",
            "68%",
            "44m³",
            "100%",
            "442,9L",
            "",
            "",
            "",


            
        ],

        # "Escopo": [
        #     "janeiro a setembro de 2022",
        #     "janeiro a setembro de 2022",
        #     "janeiro a setembro de 2022",
        #     "janeiro a setembro de 2022",
        #     "",
        #     "",
        #     "janeiro a setembro de 2022"
        #     "",
        #     "",
        #     "",
        #     "306-5 Waste directed to disposal",
        #     "306-4 Waste diverted from disposal",
        #     "303-5a Water consumption",
        #     "",
        #     "302-1 Energy consumption within the organization",
        #     "",
        #     "",
        #     "306-3 Waste generated",
        # ],

        # "GRI Standard Disclosure": [

        # ],

        # "ODS": [
        #     "12, 2",
        #     "12, 2",
        #     "12, 2",
        #     "12, 5",
        #     "",
        #     "",
        #     "12, 5",
        #     "",
        #     "",
        #     "",
        #     "12, 5",
        #     "12, 5",
        #     "12, 2",
        #     "12, 2",
        #     "12, 2",
        #     "12, 4",
        #     "12, 4",
        #     "12, 5",
        # ]
    }
)

df.to_csv("dados_socioamb.csv", index=False)