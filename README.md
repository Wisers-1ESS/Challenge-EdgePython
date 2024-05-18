# SPRINTS - TECH MAHINDRA (Python e Edge)

### Sobre o projeto

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