import json
from datetime import datetime

class Transacao:
    def __init__(self, tipo, valor, descricao, data=None):
        self.tipo = tipo
        self.valor = valor
        self.descricao = descricao
        self.data = data if data else datetime.now().strftime('%d/%m/%Y %H:%M')

    def __str__(self):
        return f'[{self.data}] {self.tipo.upper()} - R$ {self.valor:.2f} ({self.descricao})'


class Carteira:
    def __init__(self):
        self.transacoes = []
        self.saldo = 0.0

    def adicionar_transacao(self, transacao: Transacao):
        if transacao.tipo == 'entrada':
            self.saldo += transacao.valor
        elif transacao.tipo == 'saida':
            self.saldo -= transacao.valor
        else:
            print("Tipo inválido. Use 'entrada' ou 'saida'.")
            return
        self.transacoes.append(transacao)

    def listar_transacoes(self):
        if not self.transacoes:
            print('Nenhuma transação registrada.')
        else:
            for t in self.transacoes:
                print(t)

    def mostrar_saldo(self):
        print(f'\nSaldo atual: R$ {self.saldo:.2f}')

    def salvar_em_arquivo(self, arquivo='financeiro.json'):
        dados = {
            'saldo': self.saldo,
            'transacoes': [
                {'tipo': t.tipo, 'valor': t.valor, 'descricao': t.descricao, 'data': t.data}
                for t in self.transacoes
            ]
        }
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print('Dados salvos com sucesso!')

    def carregar_de_arquivo(self, arquivo='financeiro.json'):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.saldo = dados['saldo']
                self.transacoes = [
                    Transacao(d['tipo'], d['valor'], d['descricao'], d['data'])
                    for d in dados['transacoes']
                ]
            print('Dados carregados com sucesso!')
        except FileNotFoundError:
            print('Nenhum histórico encontrado. Criando novo arquivo...')
        except Exception as e:
            print(f'Erro ao carregar dados: {e}')



def menu():
    carteira = Carteira()
    carteira.carregar_de_arquivo()

    while True:
        print('\n==== CONTROLE FINANCEIRO PESSOAL ====')
        print('1 - Adicionar Entrada')
        print('2 - Adicionar Saída')
        print('3 - Listar Transações')
        print('4 - Mostrar Saldo')
        print('5 - Salvar e Sair')
        print('======================================')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            valor = float(input('\nDigite o valor da entrada: '))
            descricao = input('Descrição: ')
            transacao = Transacao('entrada', valor, descricao)
            carteira.adicionar_transacao(transacao)

        elif opcao == '2':
            valor = float(input('\nDigite o valor da saída: '))
            descricao = input('Descrição: ')
            transacao = Transacao('saida', valor, descricao)
            carteira.adicionar_transacao(transacao)

        elif opcao == '3':
            carteira.listar_transacoes()

        elif opcao == '4':
            carteira.mostrar_saldo()

        elif opcao == '5':
            carteira.salvar_em_arquivo()
            print('Saindo... ')
            break

        else:
            print('Opção inválida! Tente novamente.')

if __name__ == '__main__':
    menu()