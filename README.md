# SPRINTS - TECH MAHINDRA (Python e Edge)

## Sobre o projeto
Você já imaginou ter um hub completo de informações sobre a Fórmula E em português? Esse projeto foi criado exatamente para isso! Combinando o poder do Arduino e Python, nosso objetivo é popularizar a Fórmula E no Brasil, fornecendo um ponto centralizado para todas as informações que você precisa sobre essa emocionante categoria de corrida.

### Funcionalidades do Projeto

- **Informações em Tempo Real**: Monitore a temperatura, velocidade e nível da bateria de um veículo em tempo real usando sensores integrados ao Arduino.
- **Próximos Eventos**: Fique por dentro dos próximos eventos da Fórmula E com detalhes sobre datas, locais e horários.
- **Equipes e Pilotos**: Acesse informações detalhadas sobre as equipes e pilotos, incluindo probabilidades de vitória e estatísticas.
- **Consumo de Energia**: Visualize dados sobre o consumo de energia dos veículos, ajudando a entender melhor a eficiência dos carros elétricos.

### Tecnologias Utilizadas

- **Arduino**: Coleta de dados de sensores de temperatura, corrente e velocidade.
- **Python**: Processamento e exibição das informações coletadas, integração com APIs para obter dados adicionais sobre a Fórmula E.
- **Colorama**: Melhora a exibição das informações no terminal, tornando os dados mais acessíveis e visualmente agradáveis.

### Objetivo do Projeto

Popularizar a Fórmula E no Brasil, tornando as informações sobre essa categoria de corrida mais acessíveis para o público em geral. Através deste projeto, esperamos aumentar o interesse e o conhecimento sobre os avanços tecnológicos e a sustentabilidade promovida pela Fórmula E.

### Como Começar

1. Clone este repositório:
    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    ```
2. Siga as instruções no README para configurar o ambiente e conectar seu Arduino.
3. Execute o código e comece a explorar as funcionalidades!

---

Sinta-se à vontade para ajustar esta descrição conforme necessário para se alinhar melhor com a visão e detalhes específicos do seu projeto.

### Execução do projeto

Para executar o projeto, siga as etapas abaixo:

1. Clone o repositório para o seu ambiente local:

    ```
    git clone https://github.com/Wisers-1ESS/Challenge-EdgePython.git
    ```

2. Navegue até o diretório do projeto:

    ```
    cd Challenge-EdgePython
    ```

3. Instale as dependências necessárias:

    ```
    pip install -r requirements.txt
    ```
4. Crie uma conta no <a href="https://console.sportradar.com/">SportRadar</a> para gerar uma chave privada da API utilizada no projeto.
    * Após entrar, acessa a área de **Applications** e selecione uma existente, ou crie uma nova.
    * Clique em ***Add Trials*** e selecione *Sports API*.
    * Pesquise **Formula E** e adicione na sua Application.
    * Uma chave API foi criada, copie ela em ***API Key***.
5. Crie um arquivo ```.env``` na raiz do projeto e adicione as seguintes linhas:
   
    ```
    API_KEY=SUA_API_KEY_AQUI
    ```
    
    * Substitua ```SUA_API_KEY_AQUI``` pela sua chave privada da <a href="https://developer.sportradar.com/racing/reference/formula-e-overview" target="_blank">API SportRadar - Formula E</a>.
    * Salve o arquivo ```.env```.

6. Execute o projeto:

    ```
    python main.py
    ```

Certifique-se de ter o Python e o pip instalados em seu ambiente antes de executar o projeto.

### Integrantes do grupo

Matheus Queiroz - RM558801
