def soma(*valores):
    return sum(valores)


def ler_numero(mensagem):
    while True:
        entrada = input(mensagem).strip()
        try:
            return int(entrada)
        except ValueError:
            print("Valor invalido. Digite um numero inteiro.")


def classificar(valor):
    if valor > 10:
        return "maior que 10"
    if valor < 10:
        return "menor que 10"
    return "igual a 10"


def main():
    primeiro = ler_numero("Digite um numero: ")
    segundo = ler_numero("Digite outro numero: ")
    resultado = soma(primeiro, segundo)
    print(f"Soma: {resultado}")
    print(classificar(resultado))


if __name__ == "__main__":
    main()
