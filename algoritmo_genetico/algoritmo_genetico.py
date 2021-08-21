#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  trabalho2_IA.py
#  
#  Copyright 2021 Brendon <Brendon@DESKTOP-238NOSS>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import random
import math

#constantes
numBits = 16 
qtdPopInicial = 10
tamMaximoPop = 20
qtdElitismo = 10
qtdGeracoes = 20
minX = -20
maxX = 20
k = 5
n = 2

def individuoBinToDecimal(binarios):
	expoente = len(binarios) - 1
	
	numeroDecimalIndividuo = 0
	for binario in binarios:
		numeroDecimalIndividuo += binario * 2**expoente
		expoente -= 1
	
	return numeroDecimalIndividuo

def encontrarX(individuo):
	numeroDecimal = individuoBinToDecimal(individuo)
	x = minX + (((maxX - minX)*numeroDecimal/2**numBits) - 1)
	return x
	
#f (x)=cos(x )∗x+2
def aplicarFuncao(individuo):
	x = encontrarX(individuo)
	resultado = math.cos(x)*x + 2
	return resultado
	
def getIndividuoAptidao(individuo):
	return [individuo, aplicarFuncao(individuo)]

def orderByAptidao(individuoAptidao):
	return individuoAptidao[1]

def gerarIndividuoAleatorio():
	individuo = [random.randint(0,1) for i in range(numBits)]
	return individuo

def aplicarCrossOver(pais):
	metadeBits = numBits//2
	filho = pais[0][:metadeBits] + pais[1][metadeBits:]
	return filho 

def aplicarMutacoes(individuos):
	for individuo in individuos:
		for i in range(len(individuo)):
			probabilidadeMutation = random.random()
			if probabilidadeMutation <= 0.01:
				individuo[i] = 0 if individuo[i] == 1 else 1 

def aplicarTorneio(individuos):
	posicoes = []
	tam = len(individuos)
	qtd = k if k < tam else tam 
		
	for i in range(qtd):
		posicao = random.randint (0,tam-1)
		
		while posicao in posicoes:
			posicao = random.randint (0,tam-1)
		
		posicoes.append(posicao)
		
	individuosSorteados = [getIndividuoAptidao(individuos[posicao]) for posicao in posicoes]
	individuosSorteados.sort(key=orderByAptidao)
	pais = individuosSorteados[:2]
	pais = [pai[0] for pai in pais]
	
	probabilidadeCrossOver = random.random()

	if probabilidadeCrossOver <= 0.6:
		for i in range(n):
			individuos.append(aplicarCrossOver(pais))
	
	#aplicarMutacoes(individuos)
	
	#probabilidadeMutation = random.random()
	
	#if probabilidadeMutation <= 0.1:
	#	for pai in pais:
	#		individuos.append(aplicarMutation(pai))
	
	
def aplicarElitismo(individuos):
	individuosAptidoes = [getIndividuoAptidao(individuo) for individuo in individuos]
	individuosAptidoes.sort(key=orderByAptidao)
	return [individuo[0] for individuo in individuosAptidoes[:qtdElitismo]]

def main(args):
	print('Iniciando a solução ...')
	print()
	
	# gerando os primeiros individuos
	print('Gerando população inicial')
	individuos = [gerarIndividuoAleatorio() for i in range(qtdPopInicial)]
	print('imprimindo individuos em tuplas (binarios, decimal, transformaPraX, apitidao)')
	[print ((individuo,individuoBinToDecimal(individuo),encontrarX(individuo), getIndividuoAptidao(individuo)[1])) for individuo in individuos]
	[print for individuo in individuos]
	
	individuosAptidoes = [getIndividuoAptidao(individuo) for individuo in individuos]
	individuosAptidoes.sort(key=orderByAptidao)
	melhorDaGeracao = individuosAptidoes[0][0]
	print()
	print('melhorDaGeracao')
	print(((melhorDaGeracao,individuoBinToDecimal(melhorDaGeracao),encontrarX(melhorDaGeracao), getIndividuoAptidao(melhorDaGeracao)[1])))
	for i in range(qtdGeracoes):
		individuos = aplicarElitismo(individuos)

		while len(individuos) < tamMaximoPop:
			aplicarTorneio(individuos)
		
		aplicarMutacoes(individuos)
		
		individuosAptidoes = [getIndividuoAptidao(individuo) for individuo in individuos]
		individuosAptidoes.sort(key=orderByAptidao)
		melhorDaGeracao = individuosAptidoes[0][0]
		
		print()
		print('melhorDaGeracao')
		print(((melhorDaGeracao,individuoBinToDecimal(melhorDaGeracao),encontrarX(melhorDaGeracao), getIndividuoAptidao(melhorDaGeracao)[1])))

		
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
