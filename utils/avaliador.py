def avaliar_codigo(codigo: str, casos_teste: list) -> str:
    try:
        for caso in casos_teste:
            entrada = caso["entrada"]
            esperado = caso["saida_esperada"]

            local_vars = {}
            exec(codigo, {}, local_vars)

            if 'Solution' not in local_vars:
                return "Classe Solution não encontrada"

            sol = local_vars['Solution']()

            exec_entrada = eval(entrada)
            resultado = sol.hasDuplicate(exec_entrada)

            if str(resultado).lower() != esperado.lower():
                return f"Erro no teste com entrada {entrada}"

        return "Sucesso"
    except Exception as e:
        return f"Erro na execução: {str(e)}"
