# Instalação com Docker
> Versão do Python utilizada na imagem é 3.13

1. Clone o repositório:

```bash
git clone https://github.com/LzLuscas/LzLuscas-gitlab-webhook-agent.git \
# \
&& cd LzLuscas-gitlab-webhook-agent
```

1. Certifique-se de ter a variável de ambiente `GITLAB_WEBHOOK_TOKEN` no seu ambiente.

2. Inicie os serviços com Docker Compose:

    1. No modo de desenvolvimento (com hot reload):
        
        ```bash
            docker-compose -f docker/docker-compose.yml watch
        ```

    2. No modo de produção:
    
        ```bash
            docker-compose -f docker/docker-compose.yml up
        ```
3. Estará disponível em http://localhost:8080.

> O endpoint do healthcheck é http://localhost:8080/

# Modo de desenvolvimento

O modo de desenvolvimento inclui o hot reload através do [Docker Compose Develop](https://docs.docker.com/reference/compose-file/develop/)

O serviço do `gitlab-webhook-agent` é reconstruído quando há mudanças no diretório `app/` e reinicia automaticamente.

O serviço do `nginx` usado como proxy-reverso é reiniciado quando há mudanças no diretório `nginx/`, o que é útil para testar mudanças na configuração do Nginx sem precisar reiniciar manualmente os serviços.

# Segurança

O uvicorn está configurado para aceitar os cabeçalhos de proxy apenas do Nginx, que atua como proxy reverso através da flag `--proxy-headers` no arquivo [docker/Dockerfile](../docker/Dockerfile).

E através da variável de ambiente `UVICORN_FORWARDED_ALLOW_IPS` no arquivo [docker/docker-compose.yml](../docker/docker-compose.yml). 

O Nginx é configurado para passar os cabeçalhos de proxy corretamente, garantindo que o uvicorn possa identificar o IP real do cliente e outras informações relevantes. 

Isso é importante para a segurança, pois impede que clientes maliciosos forjem cabeçalhos de proxy e enganem o servidor sobre a origem das requisições. E garante o correto redirecionamento e roteamento das requisições para o serviço do `gitlab-webhook-agent`.

Além disso, o container do `gitlab-webhook-agent` é executado com um usuário não-root, em uma imagem distroless, o que aumenta a segurança ao reduzir a superfície de ataque e limitar os privilégios do processo. 

Os arquivos do projeto são copiados para o container e as permissões são ajustadas para garantir que o processo possa ler os arquivos necessários sem precisar de privilégios elevados-seguindo os princípios [Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege).

O Nginx utiliza a imagem oficial do Nginx [nginxinc/nginx-unprivileged](https://hub.docker.com/r/nginxinc/nginx-unprivileged) na versão `1.29.5` atual de **13/02/2026**, que é uma imagem otimizada e segura para execução de servidores web, garantindo que o Nginx seja executado com privilégios mínimos, aumentando a segurança do ambiente.

# Proxy reverso

O Nginx está configurado para agir como um proxy reverso.

> As configurações de upstream e rate limiting estão definidas no arquivo [nginx/default.conf](../nginx/default.conf).

# Balanceamento de carga
O **upstream** `gitlab-webhook-agent` é definido para apontar para o serviço do `gitlab-webhook-agent` no Docker Compose, permitindo que o Nginx encaminhe as requisições realizando o balanceamento de carga para o serviço correto.

O escalonamento horizontal é automático, através da resolução de nomes pelo DNS interno do Docker.

# Rate limiting
O Nginx está configurado para limitar a taxa de requisições usando o módulo [limit_req](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html).

As requisições são limitadas a ***10*** requisições por segundo por IP, com um burst de ***5*** requisições e um atraso de ***5*** segundos para requisições adicionais.

# Considerações finais

Embora esta configuração seja adequada e talvez **OVERKILL** para o ambiente de desenvolvimento, ela é projetada para ser facilmente adaptável para ambientes de produção, garantindo que as melhores práticas de segurança e desempenho sejam seguidas desde o início do desenvolvimento.