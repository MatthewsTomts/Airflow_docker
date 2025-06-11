
## 📚 Qual a finalidade do projeto?

Esse projeto foi criado com o intuito de colocar em prática os conteúdos aprendidos sobre as ferramentas Airflow e Spark. Nele é realizado o tratamento de dados presentes em um [arquivo csv](https://github.com/MatthewsTomts/Airflow_docker/blob/main/data/sample_with_errors_100.csv), em seguida exportar os dados para um arquivo no formato parquet e realizado o upload na ferramenta Minio e banco de dados PostgreSQL. 

---

<br>

## 💻 Tecnologias ultilizadas

- **🐘 PostgreSQL:** Ferramenta de banco de dados relacional;
- **⭐ Spark:** Ferramenta para tratamento e manipulação de dados;
- **🟇  Airflow:** Orquestração de tarefas, altamente utilizado com tarefas de ETL;
- **🐳 Docker:** Permite a criação e execução de ambiente isolados para aplicações e processos;
- **🐍 Python:** Linguagem de programação utilizada principalmente para processos de ETL;
- **🦢 Minio:** Permite o deploy e utilização de servidor de armazenamento de objetos, utilizando o padrão de API e uso do S3;
- **🖽  Parquet:** Formato de arquivo otimizado para consulta de dados, utilizando formato de armazenamento em colunas;
- **𝚇  CSV:** Formato de arquivo humano-legível, utilizado para consultas simples e com armazenamento em linhas.


---

<br>

## Estrutura do Repositório

- **/dags/aulas:**    

    Possui os arquivos de definição das DAGs criadas durante o período de estudo da ferramente Airflow.
    Veja: [`/dags/aulas`](https://github.com/MatthewsTomts/Airflow_docker/tree/main/dags/aulas)

- **/dags/projeto_airflow:**

    Possui os arquivos de definição da DAG criada para o projeto prático que combina a utilização das ferramentas Airflow e Spark. 
    veja: [`/dags/projeto_airflow`](https://github.com/matthewstomts/airflow_docker/tree/main/dags/projeto_airflow)

- **docker-compose.yaml**

    Arquivo de configuração do ambiente de execução Airflow
    Veja: [`docker-compose.yaml`](https://github.com/MatthewsTomts/Airflow_docker/blob/main/docker-compose.yaml)

- **Dockerfile**

    Arquivo para customização (extensão) da imagem base do Airflow, adicionando a biblioteca do PySpark 
    Veja: [`Dockefile`](https://github.com/MatthewsTomts/Airflow_docker/blob/main/Dockerfile)

- **/data**

    Pasta de armazenamento dos arquivos de dados utilizados durante as aulas e o projeto
    Veja: [`/data`](https://github.com/MatthewsTomts/Airflow_docker/tree/main/data)

---

<br>

## Como executar

### Opcional

1. Crie as variáveis de ambiente ```_AIRFLOW_WWW_USER_USERNAME``` e ```_AIRFLOW_WWW_USER_PASSWORD```. Caso as variáveis não sejam criadas, o usuário e senha do Airflow terão valor "airflow" por padrão.  

### Passo a Passo

2. Certifique-se de ter o Docker instalado.
3. No terminal, dentro do diretório do repositório, execute (substituindo o nome e a tag):
   
   ```sh
   docker build . --tag extending_airflow:latest 
   ```

4. Com a imagem personalizada criada, execute os containers utilizando:

    ```sh
    docker compose up -d 
    ```

5. Utilize o comando `docker ps` para identificar o id do container executando o postgres, acesse o container utilizando o comando `docker exec -it <id-do-container> bash`
6. Ao acessar o container do postgres, acesse o banco utilizando `psql -U airflow` e execute o comando `CREATE DATABASE test;`
7. Acesse o Airflow, na página `https://localhost:8080` utilizando o valor definido nas variáveis ou utilize o valor padrão
8. Na aba Admin, acesse a opção conexões nela realize a criação de uma nova conexão do tipo "postgres", adicione as variáveis 
    ```
    host 'postgres'
    login <user-definido-em-docker-compose>
    senha <senha-definido-em-docker-compose>
    port 5432
    database test 
    ```
9. Ao navegar para a aba de DAG, é possível visualizar as DAGs criadas e executá-las

### Projeto

10. Para a execução do projeto, que possui o nome de DAG "Projeto_postgres", é necessário a execução da feramenta Minio (Modifique o usuário e a senha):
    ```sh
    docker run \
    --network=airflow_docker_default \
    -p 9000:9000 \
    -p 9001:9001 \
    --user $(id -u):$(id -g) \
    --name minio1 \
    -e "MINIO_ROOT_USER=ROOTUSER" \
    -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
    -v ${HOME}/minio/data:/data \
    quay.io/minio/minio server /data --console-address ":9001"
    ```

11. Acesse o link disponibilizado na execução acima com a identificação "API", realize o login e a criação de um novo bucket nomeando o "airflow" 
12. Retorne a página de conexões e crie uma nova conexão do tipo "aws", adicione o usuário ao campo `AWS Access Key ID` e a senha ao `AWS Secret Access Key` e no campo `Extra Fields JSON` adicione o seguinte JSON:
    ```sh
    {
        "endpoint_url": "http://minio1:9000"
    }
    ```
13. Com esse passos é possível acionar a DAG do projeto.
