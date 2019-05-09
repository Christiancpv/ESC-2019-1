import os, sys


# Os dicionarios representam as 3 partes de uma isntrucao C
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


#Tabela de Simbolos. E possivel adicionar novos simbolos a tabela
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }

for i in range(0,16):
  label = "R" + str(i)
  table[label] = i


local_das_variaveis = 16    # Proximo local de memoria disponivel para as variaveis
asm_arq = 'RectL'    # Nome do arquivo a ser traduzido


def limpar(linha):
# Remove comentarios(//), espacos em branco(' ') e quebra de linhas('/n')

  char = linha[0]
  if char == "\n" or char == "/":
    return ""
  elif char == " ":
    return limpar(linha[1:])
  else:
    return char + limpar(linha[1:])


def normalize(linha):
# Normaliza instrucoes do tipo c adicionando os campos null,dest e jump


  linha = linha[:-1]
  if not "=" in linha:
    linha = "null=" + linha
  if not ";" in linha:
    linha = linha + ";null"
  return linha


def adcionarVariaveis(label):
# Aloca a memoria para novas variaveis

  global local_das_variaveis
  table[label] = local_das_variaveis
  local_das_variaveis += 1
  return table[label]


def TraduzirA(linha):
# Traduz uma instrucao ao para um int caso seja necessario
# Traduz para instrucao de maquina

  if linha[1].isalpha():
    label = linha[1:-1]
    valorA = table.get(label, -1)
    if valorA == -1:
      valorA = adcionarVariaveis(label)
  else:
    valorA = int(linha[1:])
  valorB = bin(valorA)[2:].zfill(16)
  return valorB
 

def TraduzirC(linha):
# Dvide uma instrucao c e traduz

  linha = normalize(linha)
  temp = linha.split("=")
  codigo_destino = dest.get(temp[0], "destFAIL")
  temp = temp[1].split(";")
  codigo_comp = comp.get(temp[0], "compFAIL")
  codigo_salto = jump.get(temp[1], "jumpFAIL")
  return codigo_comp, codigo_destino, codigo_salto


def definirTipo(linha):
# Define se a instrucao recebida e do tipo C ou A

  if linha[0] == "@":
    return TraduzirA(linha)
  else:
    codigos = TraduzirC(linha)
    return "111" + codigos[0] + codigos[1] + codigos[2]


def primeiraVarredura():


  asm_file = open(asm_arq + ".asm")
  hack_file = open(asm_arq + ".tmp", "w")

  numero_de_linha = 0
  for linha in asm_file:
    sline = limpar(linha)
    if sline != "":
      if sline[0] == "(":
        label = sline[1:-1]
        table[label] = numero_de_linha
        sline = ""
      else:
        numero_de_linha += 1
        hack_file.write(sline + "\n")

  asm_file.close()
  hack_file.close()


def assemble():
# Traduz para hack

  asm_file = open(asm_arq + ".tmp")
  hack_file = open(asm_arq + ".hack", "w")

  for linha in asm_file:
    tlinha = definirTipo(linha)
    hack_file.write(tlinha + "\n")

  asm_file.close()
  hack_file.close()
  os.remove(asm_arq + ".tmp")


primeiraVarredura()
assemble()

# Este codigo foi traduzido para melhor entendimento. O codigo original pode ser encontrado em:
#https://github.com/rose/nand2tetris/blob/master/assembler.py