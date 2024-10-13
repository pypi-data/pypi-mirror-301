import mysql.connector
import re
import json
import time


class DatabaseManager:
    def __init__(self, connection_string, tabela = None, pprint = None):
        # Extrai os parâmetros da string de conexão usando regex
        self.tabela = tabela
        self.ultima_chamada = 0
        if pprint:
            self.pprint = pprint
        else:
            self.pprint = print        
        self.params = self.parse_connection_string(connection_string)
        
        # Conectando ao banco de dados usando os parâmetros extraídos
        self.conexao = mysql.connector.connect(
            host=self.params['host'],
            user=self.params['user'],
            password=self.params['password'],
            port=self.params['port'],
            database=self.params['database']
        )
        self.cursor = self.conexao.cursor()

    def parse_connection_string(self, connection_string):
        # Regex para extrair host, user, password, port e database da string de conexão
        pattern = r'-h(?P<host>[\w\.]+) -u(?P<user>\w+) -p(?P<password>[\w]+) --port (?P<port>\d+) .+ (?P<database>\w+)'
        match = re.search(pattern, connection_string)
        if not match:
            raise ValueError("A string de conexão não está no formato correto.")
        
        return match.groupdict()

    def criar_tabela(self, tabela, colunas):
        """
        Cria uma tabela com um ID automático e colunas definidas pelo usuário.

        :param tabela: Nome da tabela.
        :param colunas: Um dicionário contendo os nomes das colunas e seus tipos, ex: {"nome_produto": "VARCHAR(255)", "valor": "DECIMAL(10, 2)"}.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora
            self.tabela = tabela
            colunas_str = ", ".join([f"{nome} {tipo}" for nome, tipo in colunas.items()])
            query = f"""
            CREATE TABLE IF NOT EXISTS {self.tabela} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {colunas_str}
            )
            """

            self.cursor.execute(query)
            self.conexao.commit()
            self.pprint(f"Tabela '{self.tabela}' criada com sucesso!")
            
        else:
            self.pprint('aguarde')        

    def criar_tabela_Json(self, tabela):
        """
        Cria uma tabela com um ID automático e colunas definidas pelo usuário.

        :param tabela: Nome da tabela.
        :param colunas: Um dicionário contendo os nomes das colunas e seus tipos, ex: {"nome_produto": "VARCHAR(255)", "valor": "DECIMAL(10, 2)"}.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            self.tabela = tabela
            query = f"""
            CREATE TABLE {self.tabela} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,  -- Identificador do usuário
                chave JSON NOT NULL    -- Dados em formato JSON
            )
            """

            self.cursor.execute(query)
            self.conexao.commit()
            self.pprint(f"Tabela '{self.tabela}' criada com sucesso!")
            
        else:
            self.pprint('aguarde')        

    def InserirJson(self,user_id, dados_json, tabela =None):
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora


            if tabela:
                self.tabela = tabela
            elif self.tabela:
                pass
            else:
                return self.pprint(f"Tabela não definida") 
            try:
                query = f"INSERT INTO {self.tabela} (user_id, chave) VALUES (%s, %s)"
                dados = (user_id, json.dumps(dados_json))  # Converte o dict Python em uma string JSON
                self.cursor.execute(query, dados)
                self.conexao.commit()
                self.pprint(f"Valores inseridos na tabela '{self.tabela}' com sucesso!")

            except mysql.connector.Error as err:
                self.pprint(f"Erro ao inserir valor JSON: {err}") 

        else:
            self.pprint('aguarde')

    def EditarJson(self, user_id, novos_dados_json, condicoes=None, tabela=None):
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            # Define a tabela se for passada
            if tabela:
                self.tabela = tabela
            elif self.tabela:
                pass
            else:
                return self.pprint(f"Tabela não definida")

            try:
                # Monta a query SQL para atualizar a coluna 'chave'
                query = f"UPDATE {self.tabela} SET chave = %s WHERE user_id = %s"

                # Se houver condições adicionais para a edição
                if condicoes:
                    query += f" AND {condicoes}"

                # Converte os novos dados em JSON e executa a query
                novos_dados = (json.dumps(novos_dados_json), user_id)
                self.cursor.execute(query, novos_dados)
                self.conexao.commit()

                self.pprint(f"Valores editados na tabela '{self.tabela}' com sucesso!")

            except mysql.connector.Error as err:
                self.pprint(f"Erro ao editar valor JSON: {err}")

        else:
            self.pprint('aguarde')

    def EditarJson1(self, id_registro, novo_json):
        """
        Edita o valor JSON em um registro específico da tabela, com base no ID.
        
        :param id_registro: O ID do registro que será editado.
        :param novo_json: O novo valor JSON que substituirá o atual.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            try:
                query = f"UPDATE {self.tabela} SET chave = %s WHERE id = %s"
                dados = (json.dumps(novo_json), id_registro)
                self.cursor.execute(query, dados)
                self.conexao.commit()
                self.pprint(f"Registro com ID {id_registro} atualizado com sucesso!")

            except mysql.connector.Error as err:
                self.pprint(f"Erro ao atualizar valor JSON: {err}") 

        else:
            self.pprint('Aguarde')            

    def LerJson(self, user_id, tabela=None):
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            # Define a tabela se for passada
            if tabela:
                self.tabela = tabela
            elif self.tabela:
                pass
            else:
                return self.pprint(f"Tabela não definida")

            try:
                # Monta a query SQL para buscar o campo 'chave' baseado no 'user_id'
                query = f"SELECT chave FROM {self.tabela} WHERE user_id = %s"
                self.cursor.execute(query, (user_id,))
                resultado = self.cursor.fetchone()

                # Verifica se há resultados
                if resultado:
                    # Converte a string JSON de volta para um dicionário Python
                    dados_json = json.loads(resultado[0])
                    return dados_json
                else:
                    self.pprint(f"Nenhum dado encontrado para user_id: {user_id}")
                    return None

            except mysql.connector.Error as err:
                self.pprint(f"Erro ao ler valor JSON: {err}")
                return None

        else:
            self.pprint('aguarde')
            return None

    def inserir_valor(self, colunas, valores):
        """
        Insere valores na tabela criada.

        :param colunas: Uma lista com os nomes das colunas onde os dados serão inseridos.
        :param valores: Uma lista ou tupla com os valores a serem inseridos.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            colunas_str = ", ".join(colunas)
            placeholders = ", ".join(["%s"] * len(valores))
            query = f"INSERT INTO {self.tabela} ({colunas_str}) VALUES ({placeholders})"
            self.cursor.execute(query, valores)
            self.conexao.commit()
            self.pprint(f"Valores inseridos na tabela '{self.tabela}' com sucesso!")
            
        else:
            self.pprint('aguarde')

    def ler_valores(self):
        """
        Lê todos os valores da tabela criada.
        """
   
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada

        if tempo_passado >= 0.5:
            self.ultima_chamada = agora
            query = f"SELECT * FROM {self.tabela}"
            self.cursor.execute(query)
            resultados = self.cursor.fetchall()
            return resultados
            # for linha in resultados:
            #     self.pprint(linha)
        
        else:
            self.pprint('aguarde')

    def editar_valor(self, coluna, novo_valor, condicao_coluna, condicao_valor):
        """
        Edita valores na tabela criada com base em uma condição.

        :param coluna: Coluna a ser editada.
        :param novo_valor: Novo valor para a coluna.
        :param condicao_coluna: Coluna usada como condição.
        :param condicao_valor: Valor da condição.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada        
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            query = f"UPDATE {self.tabela} SET {coluna} = %s WHERE {condicao_coluna} = %s"
            self.cursor.execute(query, (novo_valor, condicao_valor))
            self.conexao.commit()
            self.pprint(f"Valor da coluna '{coluna}' atualizado para {novo_valor} na tabela '{self.tabela}'.")

        else:
            self.pprint('aguarde')

    def deletar_valor(self, condicao_coluna, condicao_valor):
        """
        Deleta um valor da tabela criada com base em uma condição.

        :param condicao_coluna: Coluna usada como condição.
        :param condicao_valor: Valor da condição.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora
            query = f"DELETE FROM {self.tabela} WHERE {condicao_coluna} = %s"
            self.cursor.execute(query, (condicao_valor,))
            self.conexao.commit()
            self.pprint(f"Valor deletado da tabela '{self.tabela}' onde {condicao_coluna} = {condicao_valor}.")

        else:
            self.pprint('aguarde')

    def exibir_tabelas(self):

        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            
            try:
                self.cursor.execute("SHOW TABLES")
                tabelas = self.cursor.fetchall()
                # tables = []
                if tabelas:
                    self.pprint("Tabelas no banco de dados:")
                    # for tabela in tabelas:
                    #     # self.pprint(tabela[0])
                    #     tables.append(tabela[0])
                    # self.pprint(tables)
                    return tabelas
                else:
                    self.pprint("Não há tabelas no banco de dados.")
                    return [["Não há tabelas no banco de dados."]]
            except mysql.connector.Error as err:
                self.pprint(f"Erro ao exibir tabelas: {err}")

        else:
            self.pprint('aguarde')        

    def exibir_colunas(self):
        """
        Exibe as colunas da tabela criada.
        """
        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora

            query = f"SHOW COLUMNS FROM {self.tabela}"
            self.cursor.execute(query)
            colunas = self.cursor.fetchall()
            self.pprint(f"Colunas da tabela '{self.tabela}':")
            self.pprint(colunas)
            self.colunas = []
            for coluna in colunas:
                self.colunas.append(coluna[0])
                self.pprint(coluna[0])
            

        else:
            self.pprint('aguarde')        

    def carregar_colunas(self):
        """
        Exibe as colunas da tabela criada.
        """

        agora = time.time()
        tempo_passado = agora - self.ultima_chamada
        if tempo_passado >= 0.5:
            self.ultima_chamada = agora
            query = f"SHOW COLUMNS FROM {self.tabela}"
            self.cursor.execute(query)
            colunas = self.cursor.fetchall()
            # self.pprint(f"Colunas da tabela '{self.tabela}':")
            # self.pprint(colunas)
            self.colunas = []
            for coluna in colunas:
                self.colunas.append(coluna[0])
                # self.pprint(coluna[0])            
            
        else:
            self.pprint('aguarde')        

    def fechar_conexao(self,e=1):
        """
        Fecha a conexão com o banco de dados.
        """
        self.cursor.close()
        self.conexao.close()
        self.pprint("Conexão com o banco de dados fechada.")
