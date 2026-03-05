def calcular_media(notas):
    if not notas:
        raise ValueError("A lista de notas nao pode estar vazia.")

    soma = 0
    for nota in notas:
        soma += nota

    media = soma / len(notas)
    return media


if __name__ == "__main__":
    numeros = [10, 8, 7, 9]
    print(calcular_media(numeros))

    try:
        print(calcular_media([]))
    except ValueError as exc:
        print(f"Erro: {exc}")
