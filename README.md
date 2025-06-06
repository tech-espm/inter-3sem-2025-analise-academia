# Projeto Interdisciplinar III - Sistemas de Informação ESPM

<p align="center">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>

# Sistema de Monitoramento de Ocupação de Zonas de Academias

### 2025-01

## Integrantes
- [André Henrique Pacheco Alves](https://github.com/andre-alves77)
- [Guilherme Orlandi de Oliveira](https://github.com/carrico05)
- [Luis Felipe Galina Degaspari](https://github.com/luisdegaspari)
- [Luiz Felipe Pimenta Berrettini](https://github.com/pimentabrrt)
- [Luiz Fernando Pazdziora Costa](https://github.com/luizpazdziora)

## Descrição do Projeto

Este projeto é um sistema de monitoramento de interesse do cliente em espaços físicos nas academias, desenvolvido como parte do projeto interdisciplinar da disciplina de Projeto Integrado III, em conjunto com todas outras disciplinas, do curso de Ciências de Dados e Negócios da ESPM (Escola Superior de Propaganda e Marketing), sob a supervisão do professor Carlos Rafael Gimenes das Neves. 
O sistema utiliza sensores presentes na unidade principal da faculdade para fazer o monitoramento e análise de interesse de espaços, com o uso dos sensores "PRESENCE DETECTOR HPD2 IP" e "Passage People Counter VS350-915M PN White" na área de lazer do local, o PCA.
O objetivo é que o sistema permita que os gerentes das academias tomem decisões de compras e rearranjamento de equipamentos na academia embasado em dados de ocupação das máquinas. Por exemplo, se uma máquina é muito utilizada e, constantemente, gera fila, comprar novas máquinas desse mesmo tipo pode ser vantajoso para o cliente. Também é possível estabelecer padrões de uso de múltiplos equipamentos pelos usuários do serviço fornecido.
O projeto foi concebido em parceria com a empresa Absolut Technologies e conta com a avaliação da Microsoft e da Pfizer, integrando tecnologia de sensores avançados a uma solução voltada para inteligência operacional em academias. Além de possibilitar decisões mais eficazes para gestores, o sistema também está alinhado com os Objetivos de Desenvolvimento Sustentável (ODS) da ONU, como saúde e bem-estar (ODS 3) e inovação e infraestrutura (ODS 9), promovendo ambientes mais eficientes e acessíveis. A plataforma também reforça práticas sustentáveis ao evitar gastos desnecessários com equipamentos subutilizados. 
O desenvolvimento seguiu a metodologia ágil SCRUM, com ciclos de entrega quinzenais e gestão colaborativa via GitHub, reforçando o compromisso com a entrega contínua e a documentação clara do progresso.

## Configuração do Projeto

Para executar, deve criar o arquivo `config.py` da seguinte forma:

```python
host = '0.0.0.0'
port = 3000
conexao_banco = 'mysql+mysqlconnector://usuario:senha@host/banco'
url_api = 'https://site.com'
```

Todos os comandos abaixo assumem que o terminal esteja com o diretório atual na raiz do projeto.

## Criação e Ativação do venv

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Execução

```
.venv\Scripts\activate
python app.py
```

## Mais Informações

https://flask.palletsprojects.com/en/3.0.x/quickstart/
https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/

# Licença

Este projeto é licenciado sob a [MIT License](https://github.com/tech-espm/inter-3sem-2025-analise-academia/blob/main/LICENSE).

<p align="right">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo-si-512.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>


flask --app app run --debug --reload

sass --watch static/scss/bootstrap.scss static/css/bootstrap.css 

fontes
https://www.allfreefonts.co/abc-favorit-font/
https://seankanedesign.gumroad.com/l/sk-modernist
https://fontshare.com/ -- satoshi
