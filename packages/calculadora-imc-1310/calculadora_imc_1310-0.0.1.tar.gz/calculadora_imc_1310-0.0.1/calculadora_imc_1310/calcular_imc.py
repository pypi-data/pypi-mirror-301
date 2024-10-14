print("\nBem vindo a Calculadora de IMC")
print("==============================")

pergunta_nome = input("Qual é o seu nome? " )
nome = f'   Olá, {pergunta_nome}'
print(f'\t\t{nome}')
idade = input (f"Qual sua idade? ")
peso = float(input("Qual seu peso (em KG)? "))
altura = float(input("Qual sua Altura (em metros e usando ponto)? "))

print("\nVamos calcular seu IMC")
print("======================")

imc = (peso / (altura * altura))

print(f"{pergunta_nome}, seu IMC é: {imc:.2f}")

if imc < 16:
	print("\n\tSeu estado é de Magreza grave\n\tProcure um médico ou nutricionista.\n")
elif imc < 17:
	print("\n\tSeu estado é de Magreza moderada\n\tPrecisa rever sua alimentação.\n")
elif imc < 18.5:
	print("\n\tSeu estado é de Magreza leve\n\tPrecisa rever sua alimentação.\n")
elif imc < 25:
	print("\n\tVocê está Saudável.\n\tParabéns!!!\n")
elif imc < 30:
	print("\n\tSeu estado é de Sobrepeso\n\tPrecisa rever sua alimentação.\n")
elif imc < 35:
	print("\n\tSeu estado é de Obesidade Grau I\n\tProcure um médico ou nutricionista.\n")
elif imc < 40:
	print("\n\tSeu estado é de Obesidade Grau II (severa)\n\tProcure um médico ou nutricionista.\n")
else:
	print("\n\tSeu estado é de Obesidade Grau III (mórbida)\n\tProcure um médico ou nutricionista.\n")